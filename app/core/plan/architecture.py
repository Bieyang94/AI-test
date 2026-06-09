from langgraph.graph import START, END
from langgraph.graph import StateGraph
from app.core.plan import whether
from app.core.model import llm
from app.core.plan.class_state import State

# 节点
# 条件边函数，根据导航测试结果是否需要改进来决定路由
def llm_navigation_test(state: State):
    """调用导航测试 LLM"""
    result = llm.model_navigation_test.invoke(f"从导航测试角度回答导航测试: {state['prompt']}")
    return {"result_navigation_test": result.content}


# 条件边函数，根据导航测试结果是否需要改进来决定路由
def llm_form_input_test(state: State):
    """调用表单输入测试 LLM"""
    result = llm.model_form_input_test.invoke(f"从表单输入测试角度回答表单输入测试: {state['prompt']}")
    return {"result_form_input_test": result.content}


# 条件边函数，根据表单输入测试结果是否需要改进来决定路由
def llm_search_filter_test(state: State):
    """调用搜索筛选测试 LLM"""
    result = llm.model_search_filter_test.invoke(f"从搜索筛选测试角度回答搜索筛选测试: {state['prompt']}")
    return {"result_search_filter_test": result.content}


# 条件边函数，根据搜索筛选测试结果是否需要改进来决定路由
def llm_crud_test(state: State):
    """调用CRUD测试 LLM"""
    result = llm.model_crud_test.invoke(f"从CRUD测试角度回答CRUD测试: {state['prompt']}")
    return {"result_crud_test": result.content}


# 条件边函数，根据CRUD测试结果是否需要改进来决定路由
def llm_upload_download_test(state: State):
    """调用上传下载测试 LLM"""
    result = llm.model_upload_download_test.invoke(f"从上传下载测试角度回答上传下载测试: {state['prompt']}")
    return {"result_upload_download_test": result.content}


# 条件边函数，根据上传下载测试结果是否需要改进来决定路由
def llm_permission_test(state: State):
    """调用权限测试 LLM"""
    result = llm.model_permission_test.invoke(f"从权限测试角度回答权限测试: {state['prompt']}")
    return {"result_permission_test": result.content}


# 条件边函数，根据权限测试结果是否需要改进来决定路由
def llm_session_test(state: State):
    """调用会话测试 LLM"""
    result = llm.model_session_test.invoke(f"从会话测试角度回答会话测试: {state['prompt']}")
    return {"result_session_test": result.content}


# 条件边函数，根据会话测试结果是否需要改进来决定路由
def llm_data_consistency_test(state: State):
    """调用数据一致性测试 LLM"""
    result = llm.model_data_consistency_test.invoke(f"从数据一致性测试角度回答数据一致性测试: {state['prompt']}")
    return {"result_data_consistency_test": result.content}


# 条件边函数，根据数据一致性测试结果是否需要改进来决定路由
def llm_messages_test(state: State):
    """调用消息测试 LLM"""
    result = llm.model_messages_test.invoke(f"从消息测试角度回答消息测试: {state['prompt']}")
    return {"result_messages_test": result.content}


# 条件边函数，根据消息测试结果是否需要改进来决定路由
def llm_i18n_test(state: State):
    """调用多语言测试 LLM"""
    result = llm.model_i18n_test.invoke(f"从多语言测试角度回答多语言测试: {state['prompt']}")
    return {"result_i18n_test": result.content}


# 条件边函数，根据多语言测试结果是否需要改进来决定路由
def llm_navigation_fallback_test(state: State):
    """调用导航回退测试 LLM"""
    result = llm.model_navigation_fallback_test.invoke(f"从导航回退测试角度回答导航回退测试: {state['prompt']}")
    return {"result_navigation_fallback_test": result.content}


def route_all_tests(state: State):
    """根据 wether 配置，返回需要执行的节点列表（并行执行）"""
    next_nodes = []

    if whether.wether_navigation_test(state):
        next_nodes.append("llm_navigation_test")
    if whether.wether_form_input_test(state):
        next_nodes.append("llm_form_input_test")
    if whether.wether_search_filter_test(state):
        next_nodes.append("llm_search_filter_test")
    if whether.wether_crud_test(state):
        next_nodes.append("llm_crud_test")
    if whether.wether_upload_download_test(state):
        next_nodes.append("llm_upload_download_test")
    if whether.wether_permission_test(state):
        next_nodes.append("llm_permission_test")
    if whether.wether_session_test(state):
        next_nodes.append("llm_session_test")
    if whether.wether_data_consistency_test(state):
        next_nodes.append("llm_data_consistency_test")
    if whether.wether_messages_test(state):
        next_nodes.append("llm_messages_test")
    if whether.wether_i18n_test(state):
        next_nodes.append("llm_i18n_test")
    if whether.wether_navigation_fallback_test(state):
        next_nodes.append("llm_navigation_fallback_test")

    return next_nodes


def consolidation_data(state: State):
    """合并数据"""


# 构建工作流
workflow_builder = StateGraph(State)

# 添加节点
workflow_builder.add_node("route_all_tests", route_all_tests)

workflow_builder.add_node("llm_navigation_test", llm_navigation_test)
workflow_builder.add_node("llm_form_input_test", llm_form_input_test)
workflow_builder.add_node("llm_search_filter_test", llm_search_filter_test)
workflow_builder.add_node("llm_crud_test", llm_crud_test)
workflow_builder.add_node("llm_upload_download_test", llm_upload_download_test)
workflow_builder.add_node("llm_permission_test", llm_permission_test)
workflow_builder.add_node("llm_session_test", llm_session_test)
workflow_builder.add_node("llm_data_consistency_test", llm_data_consistency_test)
workflow_builder.add_node("llm_messages_test", llm_messages_test)
workflow_builder.add_node("llm_i18n_test", llm_i18n_test)
workflow_builder.add_node("llm_navigation_fallback_test", llm_navigation_fallback_test)

workflow_builder.add_node("consolidation_data", consolidation_data)

# 从 START 路由到所有需要执行的测试节点（并行）
workflow_builder.add_edge(
    START,
    "route_all_tests",
)

# 添加条件边来连接节点
workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_navigation_test,
    "llm_navigation_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_form_input_test,
    "llm_form_input_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_search_filter_test,
    "llm_search_filter_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_crud_test,
    "llm_crud_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_upload_download_test,
    "llm_upload_download_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_permission_test,
    "llm_permission_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_session_test,
    "llm_session_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_data_consistency_test,
    "llm_data_consistency_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_messages_test,
    "llm_messages_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_i18n_test,
    "llm_i18n_test"
)

workflow_builder.add_conditional_edges(
    "route_all_tests",
    whether.wether_navigation_fallback_test,
    "llm_navigation_fallback_test"
)

workflow_builder.add_edge(
    "llm_navigation_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_form_input_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_search_filter_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_crud_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_upload_download_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_permission_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_session_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_data_consistency_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_messages_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_i18n_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "llm_navigation_fallback_test",
    "consolidation_data"
)

workflow_builder.add_edge(
    "consolidation_data",
    END
)
# 编译工作流
workflow = workflow_builder.compile()

def export_workflow_png(output_path: str = "workflow.png") -> str:
    png_bytes = workflow.get_graph().draw_mermaid_png()
    with open(output_path, "wb") as f:
        f.write(png_bytes)
    return output_path
