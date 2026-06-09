

question = ("""
# Time 模块需求文档 (PRD)

## 1. 模块概述

- **模块名称**: time
- **模块文件**: `adk-docx/app/tools/time.py`
- **模块功能**: 获取指定时区的当前时间

## 2. 功能需求

### 2.1 主要功能

#### F1: 获取当前时间
- **功能描述**: 获取指定时区的当前时间字符串
- **输入参数**:
  - `tz_name` (str): IANA 时区名称，例如 "Asia/Shanghai", "America/New_York"
- **返回格式**: `dict[str, Any]`，包含：
  - `data.time`: ISO 格式时间字符串 (例如 "2023-10-01 12:00:00+08:00")
  - `data.timezone`: 时区名称
  - `message`: 操作结果消息

### 2.2 成功场景

| 场景 | 输入 | 预期输出 |
|------|------|----------|
| 有效时区-亚洲 | "Asia/Shanghai" | 返回上海当前时间，timezone为"Asia/Shanghai"，message为"success" |
| 有效时区-美洲 | "America/New_York" | 返回纽约当前时间，timezone为"America/New_York"，message为"success" |
| 有效时区-欧洲 | "Europe/London" | 返回伦敦当前时间，timezone为"Europe/London"，message为"success" |
| 有效时区-UTC | "UTC" | 返回UTC时间，timezone为"UTC"，message为"success" |
| 有效时区-带偏移 | "Pacific/Honolulu" | 返回夏威夷时间（UTC-10），message为"success" |

### 2.3 异常场景

| 场景 | 输入 | 预期输出 |
|------|------|----------|
| 无效时区名称 | "Invalid/Timezone" | 返回UTC时间，timezone为"UTC"，message包含错误提示 |
| 空字符串时区 | "" | 返回UTC时间，timezone为"UTC"，message包含错误提示 |
| None时区 | None | 可能抛出异常或返回UTC时间（取决于实现） |
| 无效格式时区 | "NotATimezone" | 返回UTC时间，timezone为"UTC"，message包含错误提示 |
| 错误格式时区 | "Asia/" | 返回UTC时间，timezone为"UTC"，message包含错误提示 |

### 2.4 边界条件

| 边界条件 | 描述 |
|----------|------|
| 有效IANA时区 | 必须支持标准IANA时区数据库中的所有时区 |
| 时区大小写 | 需要验证大小写是否敏感（如 "Asia/Shanghai" vs "asia/shanghai"） |
| 夏令时时区 | 需要正确处理夏令时切换时的时区 |
| 历史时区 | 某些历史时区名称可能已被废弃 |

## 3. 技术实现细节

### 3.1 依赖项
- `datetime`: Python 内置日期时间模块
- `zoneinfo.ZoneInfo`: Python 3.9+ 时区支持
- `zoneinfo.ZoneInfoNotFoundError`: 时区未找到异常
- `app.core.config.get_settings`: 应用配置

### 3.2 核心逻辑

```python
def get_current_time(tz_name: str) -> dict[str, Any]:
    # 1. 尝试使用提供的时区名称创建 ZoneInfo 对象
    # 2. 如果成功，返回当前时间（ISO格式）和时区名称
    # 3. 如果抛出 ZoneInfoNotFoundError，使用 UTC 作为默认时区
    # 4. 返回包含数据和消息的字典
```

### 3.3 异常处理
- `ZoneInfoNotFoundError`: 当提供的时区名称无效时捕获，并回退到 UTC

## 4. 返回值结构

### 4.1 成功返回值
```python
{
    "data": {
        "time": "2023-10-01T12:00:00+08:00",  # ISO 格式
        "timezone": "Asia/Shanghai"
    },
    "message": "success"
}
```

### 4.2 异常返回值
```python
{
    "data": {
        "time": "2023-10-01T04:00:00+00:00",
        "timezone": "UTC"
    },
    "message": "无效的时区名称 'Invalid/Timezone'，将使用 UTC 作为默认时区。"
}
```

## 5. 测试用例设计

### 5.1 功能测试用例

| 用例ID | 描述 | 输入 | 预期结果 |
|--------|------|------|----------|
| TC01 | 有效亚洲时区 | "Asia/Shanghai" | 返回上海时间，message="success" |
| TC02 | 有效美洲时区 | "America/New_York" | 返回纽约时间，message="success" |
| TC03 | 有效欧洲时区 | "Europe/London" | 返回伦敦时间，message="success" |
| TC04 | UTC时区 | "UTC" | 返回UTC时间，message="success" |
| TC05 | 无效时区名称 | "Invalid/Zone" | 返回UTC时间，message包含错误信息 |
| TC06 | 空字符串时区 | "" | 返回UTC时间，message包含错误信息 |

### 5.2 边界测试用例

| 用例ID | 描述 | 输入 | 预期结果 |
|--------|------|------|----------|
| TC07 | None输入 | None | 测试异常处理 |
| TC08 | 特殊时区 | "Pacific/Honolulu" | 返回夏威夷时间 |
| TC09 | 大小写变体 | "asia/shanghai" | 验证大小写是否敏感 |
| TC10 | 数字时区 | "GMT+8" | 验证是否支持数字格式 |

### 5.3 回归测试用例

| 用例ID | 描述 | 输入 | 预期结果 |
|--------|------|------|----------|
| TC11 | 多次调用一致性 | 同一时区多次调用 | 返回的时间应该递增 |
| TC12 | 返回值类型 | 任意有效时区 | 返回dict类型 |

## 6. 质量指标

- **行覆盖率目标**: >= 95%
- **分支覆盖率目标**: >= 90%
- **功能测试覆盖**: 100% 功能点
- **异常处理覆盖**: 100% 异常类型
""")