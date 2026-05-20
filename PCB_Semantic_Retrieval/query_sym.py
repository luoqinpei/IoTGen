#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provide API for querying symbol information from the library according to user requests.
"""

import os, sys, json, re
import argparse
from pathlib import Path
from typing import List, Dict, Set

project_path = os.environ.get("PROJECT_PATH")
if project_path:
    sys.path.append(project_path)

from modules.utils.llm_interface import GetLLMInterface
from PCB_Semantic_Retrieval.lib_helper import GlobalHybridIndex, GlobalHybridSearcher, build_query_from_extended_symbol
from pydantic import BaseModel, Field
from PCB_Semantic_Retrieval.symbol_extension import ExtendedSymbols
from modules.utils.custom_logger import setup_logger

class SymbolInfo(BaseModel):
    category: str = Field(description="Category of the symbol")
    function_name: str = Field(alias="function name", description="Function name of the symbol")

    model_config = {
        "validate_by_name": True,
        "populate_by_name": True,
    }

class SymbolInfos(BaseModel):
    symbols: list[SymbolInfo] = []

logger = setup_logger()

class Search_Symbol_Info(BaseModel):
    """
    SymbolInfo is a class that defines the properties of a symbol in the schematic editor.
    """
    symbols: list[ExtendedSymbols] = []

class SymbolInfoResponse(BaseModel):
    """
    Response model for symbol information query.
    """
    selected_symbols: List[str]

# Paths to the generated files from the tree builder:
#   - lib_tree.json             (category -> function -> lib_id -> [symbol_names])
#   - lib_tree.taxonomy.json    (categories, functions_by_category)
SYMBOL_REPO_PATH = Path(project_path) / "PCB_Semantic_Retrieval" / "component_repository.json"
SYMBOL_TAXONOMY_PATH = Path(project_path) / "PCB_Semantic_Retrieval" / "component_repository.taxonomy.json"
SYMBOL_INDEX_PATH = Path(project_path) / "PCB_Semantic_Retrieval" / "symbol_index.jsonl"
SQLITE_DB_PATH = Path(project_path) / ".cache_symbol_index" / "fts.db"


# ---------- Helpers to load JSON files ----------

def _load_taxonomy() -> Dict:
    """Load taxonomy JSON: { 'categories': [...], 'functions_by_category': {...} }."""
    path = Path(SYMBOL_TAXONOMY_PATH)
    if not path.is_file():
        raise FileNotFoundError(f"Taxonomy file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_tree() -> Dict:
    """Load tree JSON: category -> function -> lib_id -> [symbol_names]."""
    path = Path(SYMBOL_REPO_PATH)
    if not path.is_file():
        raise FileNotFoundError(f"Symbol repo (tree) file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_selection(response: str, valid_options: List[str]) -> List[str]:
    """
    Parse an LLM response (comma/newline/semicolon separated) into a list of
    valid options (case-insensitive, with some fuzzy matching).
    """
    if not response:
        return []

    tokens = re.split(r"[,\n;]+", response)
    selected: List[str] = []
    lower_valid = [v.lower() for v in valid_options]

    for token in tokens:
        t = token.strip()
        if not t:
            continue
        t_low = t.lower()

        # 1) exact (case-insensitive) match
        found = None
        for v, v_low in zip(valid_options, lower_valid):
            if v_low == t_low:
                found = v
                break

        # 2) substring-based fallback (e.g. "buck regulator" vs "Buck Regulator")
        if found is None:
            for v, v_low in zip(valid_options, lower_valid):
                if v_low in t_low or t_low in v_low:
                    found = v
                    break

        if found and found not in selected:
            selected.append(found)

    return selected

def build_local_msg(user_request: str, symbol_info_list: list[SymbolInfo]) -> list[dict]:
    """
    line_obj: The JSON object representing one symbol entry.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an expert in PCB design and KiCad symbol libraries. "
                "Given user's request, give a list of all the possible symbols that match the request, including the "
                "following fields: symbol name (type), possible footprint, technical specification, the symbol function, "
                "and the application according the request."
            ),
        },
        {
            "role": "user",
            "content": (
                "Here is one symbol entry from my index. "
                "Please infer the requested fields:\n\n"
                f"{user_request}\n\n"
                "You must refer to the following symbol information list to help you identify the exact symbols\n"
                f"{symbol_info_list}\n\n"
                "For each function, please provide your answer in JSON format with the following keys: "
                "'function_name', 'possible footprint', 'technical_specification', 'function', 'application'. "
            ),
        },
    ]

# ---------- Public API ----------

def get_category_list() -> list:
    """
    Get the list of categories from the taxonomy file.

    Returns:
        List[str]: A list of categories.
    """
    tax = _load_taxonomy()
    categories = tax.get("categories", [])
    # Optional: sort for stability
    return list(categories)


def get_function_list(category: str) -> list:
    """
    Get the list of functions from the taxonomy file for a given category.

    Args:
        category (str): Category name.

    Returns:
        List[str]: A list of functions belonging to that category.
    """
    tax = _load_taxonomy()
    fbc = tax.get("functions_by_category", {})
    return list(fbc.get(category, []))

def choose_from_topK_symbols(user_query: str, candidate_symbols: List[str], topK: int = 5) -> List[str]:
    """
    Given a user query and a list of candidate symbols, use LLM to choose the most relevant symbol.

    Args:
        user_query (str): The user's query regarding symbol information.
        candidate_symbols (List[str]): A list of candidate symbol names.

    Returns:
        str: The chosen symbol name.
    """

    prompt = f"""You are an expert in PCB design and KiCad symbol libraries. Based on the following user query:
\"\"\"{user_query}\"\"\"
And the following list of candidate symbols in the format of 'lib_id:symbol_name':
{candidate_symbols}
Please choose the most top {topK} relevant symbol that best matches the user's query. Provide the list of symbol names as your answer."""
    
    llm = GetLLMInterface(model_name="gpt-5", model_provider="OpenRouter")
    msg = [{"role": "user", "content": prompt}]
    response = llm.get_json_response(msg, SymbolInfoResponse)

    return response

def retrieve_symbols_with_llm_and_hybrid(
    user_query: str,
    symbol_info_list: List[SymbolInfo],
    hybrid_searcher: GlobalHybridSearcher,
    model_name: str = "gpt-5",
    model_provider: str = "OpenRouter",
    ann_fts_topk: int = 20,
    llm_topk_per_symbol: int = 5,
) -> List[str]:
    """
    Full pipeline:

    1) Use LLM (Search_Symbol_Info) to propose a list of "ideal" symbols
       (ExtendedSymbols) for the user's query + function list.

    2) For each ExtendedSymbols, build a query string and run hybrid
       FTS+ANN search on the *real* symbol library to obtain topK
       candidate 'lib_id:symbol_name'.

    3) For each candidate list, call choose_from_topK_symbols() to ask LLM
       to select the top-N (e.g., 5) most relevant real symbols.

    4) Aggregate all chosen symbols and return as the final result list.
    """

    # ----- Step 1: Call LLM to get ExtendedSymbols list -----
    llm = GetLLMInterface(model_name=model_name, model_provider=model_provider)
    
    msg_symbols = build_local_msg(user_query, symbol_info_list)
    logger.info(f"LLM message for symbol proposal: {msg_symbols}")
    response = llm.get_json_response(
        msg_symbols,
        Search_Symbol_Info
    )

    if isinstance(response, tuple):
        response_symbols = response[1]
    else:
        response_symbols = response

    proposed_symbols: List[ExtendedSymbols] = response_symbols.symbols or []
    logger.debug(f"Proposed symbols from LLM: {proposed_symbols}")

    if not proposed_symbols:
        return []

    final_results: Set[str] = set()

    # ----- Step 2 & 3: For each proposed symbol, run hybrid search + LLM re-ranking -----
    for sym in proposed_symbols:
        # 2(a) Build query from this ExtendedSymbols
        query_for_this_sym = build_query_from_extended_symbol(sym)

        # 2(b) Hybrid search in global library -> candidate 'lib_id:symbol_name'
        candidate_symbols: List[str] = hybrid_searcher.search(
            query_for_this_sym,
            topk=ann_fts_topk,
        )
        if not candidate_symbols:
            continue
        
        logger.debug(f"Candidate symbols for '{sym}': {candidate_symbols}")
        # 3) LLM chooses the most relevant subset from candidates
        chosen = choose_from_topK_symbols(
            user_query=user_query,
            candidate_symbols=candidate_symbols,
            topK=llm_topk_per_symbol,
        )

        # Depending on your SymbolInfoResponse, chosen might be an object;
        # here we assume choose_from_topK_symbols returns a List[str].
        if isinstance(chosen, list):
            for pk in chosen:
                final_results.add(pk)
        else:
            # If choose_from_topK_symbols returns a Pydantic model,
            # adapt accordingly, e.g. chosen.symbols
            try:
                for pk in chosen.symbols:  # type: ignore[attr-defined]
                    final_results.add(pk)
            except AttributeError:
                pass

    # Convert set to list; you may sort if you want deterministic order
    return list(final_results)


def query_symbol_info(user_query: str, model_name: str = "gpt-5", model_provider: str = "OpenRouter") -> List[str]:
    """
    Query symbol information from the library according to user requests.

    Args:
        user_query (str): The user's query regarding symbol information.
        model_name (str): LLM model name passed to GetLLMInterface.
        model_provider (str): LLM provider name.

    Returns:
        List[str]: A list of "lib_id:symbol_id" strings that match the query.
    """
    llm = GetLLMInterface(model_name=model_name, model_provider=model_provider)

    logger.info(f"User query: {user_query}")

    # ----- Step 0: Load taxonomy + tree once -----
    categories = get_category_list()
    taxonomy = _load_taxonomy()
    functions_by_category: Dict[str, List[str]] = taxonomy.get("functions_by_category", {})
    tree = _load_tree()  # category -> function -> lib_id -> [names]

#     # ----- Step 1: Ask LLM which categories are relevant -----
#     category_selection_prompt = f"""You are helping to select symbol categories for a PCB design.

# Given the following list of categories:
# {categories}

# Select the categories that are relevant to the following user query:
# \"\"\"{user_query}\"\"\"

# Provide your answer as a comma-separated list of categories (using the exact names from the list).
# Note that for almost all circuits, the categories of "Passive" and "Power" are essential and should be included unless the user specifically excludes them.
# """
#     msg_cat = [{"role": "user", "content": category_selection_prompt}]
#     response_cat = llm.get_string_response(msg_cat)

#     selected_categories = _parse_selection(response_cat, categories)

#     if not selected_categories:
#         # If nothing selected, you could fallback to "all categories" or return empty.
#         return []

#     logger.info(f"Selected categories: {selected_categories}")
#     # ----- Step 2: Gather all functions for the selected categories -----
#     function_list: List[str] = []
#     func_to_cats: Dict[str, Set[str]] = {}

#     for category in selected_categories:
#         funcs = functions_by_category.get(category, [])
#         for f in funcs:
#             function_list.append(f)
#             func_to_cats.setdefault(f, set()).add(category)

#     # If no functions at all, nothing to return.
#     if not function_list:
#         return []

#     # ----- Step 3: Ask LLM which functions are relevant -----
#     function_selection_prompt = f"""You are helping to select symbol functions for a PCB design.

# Given the following list of functions:
# {function_list}

# Select the functions that are relevant to the following user query:
# \"\"\"{user_query}\"\"\"

# Provide your answer as a comma-separated list of functions (using the exact names from the list).
# Note that for almost all circuits, functions related to "Resistor", "Capacitor", "Inductor", and "Global Power" are essential and should be included unless the user specifically excludes them.
# """
#     msg_func = [{"role": "user", "content": function_selection_prompt}]

#     logger.debug(f"LLM message for function selection: {msg_func}")
    
#     response_func = llm.get_string_response(msg_func)

#     selectted_function_list = _parse_selection(response_func, function_list)
#     if not selectted_function_list:
#         return []
    
#     logger.info(f"Selected functions: {selectted_function_list}")

    selection_prompt = f"""You are helping to select symbol functions for a PCB design.
    Here are the categories:{categories}, and here is the function list: {functions_by_category}.
    You need to think carefully about the user query {user_query}, analyze what parts are required in the circuit, and provide a list of symbol information following the format: category, function_name.
    For example, for a power regulator circuit, we have the following symbol information:
    [{{"category": "Voltage Regulator", "function name": "Linear Voltage Regulator"}}, {{"category": "Power", "function name": "Global Power"}}, {{"category": "Passive", "function name": "Capacitor"}}].
    Please provide your answer in JSON format.
    """

    msg_selection = [{"role": "user", "content": selection_prompt}]
    # logger.debug(f"LLM message for function selection: {msg_selection}")
    response, obj = llm.get_json_response(msg_selection, SymbolInfos)
    symbol_info_list = obj.symbols or []

    final_symbol_list = retrieve_symbols_with_llm_and_hybrid(user_query=user_query,
                                                             symbol_info_list=symbol_info_list,
                                                             hybrid_searcher=GlobalHybridSearcher(GlobalHybridIndex(SYMBOL_INDEX_PATH, SQLITE_DB_PATH)),
                                                             model_name=model_name,
                                                             model_provider=model_provider)

    logger.info(f"Final selected symbols: {final_symbol_list}")
    
    print(final_symbol_list)
    return final_symbol_list

def parse_args():
    parser = argparse.ArgumentParser(description="Query symbol information from the library.")
    parser.add_argument("--user_query", help="User query for symbol retrieval")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    user_query = args.user_query
    query_symbol_info(user_query)