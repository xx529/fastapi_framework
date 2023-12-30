# Web项目结构

## 关于参数配置

### 优先级
1. environment variable
2. ./settings.yaml 
3. ./app/config/default.yaml

### 命名规则
1. `settings.yaml` 与 `default.yaml` 结构一样
2. 环境变量中的 `APP_APISERVER__PORT` 等价与以下 `.yaml` 文件配置
```yaml
apiserver:
  port: 8080
```
