
from typing import TypedDict, Optional


class State(TypedDict):
    prompt: str
    result_navigation_test: Optional[str]
    result_form_input_test: Optional[str]
    result_search_filter_test: Optional[str]
    result_crud_test: Optional[str]
    result_upload_download_test: Optional[str]
    result_permission_test: Optional[str]
    result_session_test: Optional[str]
    result_data_consistency_test: Optional[str]
    result_messages_test: Optional[str]
    result_i18n_test: Optional[str]
    result_navigation_fallback_test: Optional[str]
