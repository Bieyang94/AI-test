
from app.core.plan.class_state import State

_NODE_MAP = {
    "navigation": "llm_navigation_test",
    "form_input": "llm_form_input_test",
    "search_filter": "llm_search_filter_test",
    "crud": "llm_crud_test",
    "upload_download": "llm_upload_download_test",
    "permission": "llm_permission_test",
    "session": "llm_session_test",
    "data_consistency": "llm_data_consistency_test",
    "messages": "llm_messages_test",
    "i18n": "llm_i18n_test",
    "navigation_fallback": "llm_navigation_fallback_test",
}


def _make_router(node_name: str):
    def route(state: State) -> str:
        return node_name
    route.__name__ = f"whether_{node_name}"
    return route


whether_navigation_test = _make_router(_NODE_MAP["navigation"])
whether_form_input_test = _make_router(_NODE_MAP["form_input"])
whether_search_filter_test = _make_router(_NODE_MAP["search_filter"])
whether_crud_test = _make_router(_NODE_MAP["crud"])
whether_upload_download_test = _make_router(_NODE_MAP["upload_download"])
whether_permission_test = _make_router(_NODE_MAP["permission"])
whether_session_test = _make_router(_NODE_MAP["session"])
whether_data_consistency_test = _make_router(_NODE_MAP["data_consistency"])
whether_messages_test = _make_router(_NODE_MAP["messages"])
whether_i18n_test = _make_router(_NODE_MAP["i18n"])
whether_navigation_fallback_test = _make_router(_NODE_MAP["navigation_fallback"])

wether_navigation_test = whether_navigation_test
wether_form_input_test = whether_form_input_test
wether_search_filter_test = whether_search_filter_test
wether_crud_test = whether_crud_test
wether_upload_download_test = whether_upload_download_test
wether_permission_test = whether_permission_test
wether_session_test = whether_session_test
wether_data_consistency_test = whether_data_consistency_test
wether_messages_test = whether_messages_test
wether_i18n_test = whether_i18n_test
wether_navigation_fallback_test = whether_navigation_fallback_test
