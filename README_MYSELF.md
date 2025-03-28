# 论文实验

```
conda create -n "llmpebase"
conda activate llmpebase
pip install .
pip install pyqt5==5.14
pip install spyder==5.4.3
pip install tables==3.8.0
pip install deepspeed==0.9.5
pip install .
pip install pydantic==1.10.16
```








# 代码修改

## 解决 llama

修改 `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/model/__init__.py`, 将 `meta_llama` 和 `llama_hf` 改为 None


## 解决 chatanywhere api 问题

修改 `llmpebase/model/LM/gpts.py`, 将 client 改为

```
self.client = OpenAI(
    api_key=os.environ.get("CHATANYWHERE_API_KEY"),  # 修改环境变量名
    base_url="https://api.chatanywhere.tech/v1"   # 替换为 ChatAnywhere 的 API 地址
)
```


## 解决画图的库问题

注释了 `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/model/thought_structure/base.py` 部分有关画图的代码

```
# Draw the graph and save to the disk
# as each node added to the graph means a new step
# if num_nodes < len(self.node_pool):
#     if self.visualizer is not None:
#         self.visualizer.visualize(
#             self.graph,
#             self.node_pool,
#             save_name=f"Growth_{growth_idx}__Step_{grow_node.step_idx + 1}",
#         )
#     growth_idx += 1
```



注释 `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/model/thought_structure/base.py` 有关画图的部分

```
# # Draw the whole graph after building
# if self.visualizer is not None:
#     self.visualizer.visualize(
#         self.graph, self.node_pool, save_name="built_structure"
#     )
```


## 改 prompt

需要改 `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/model/__init__.py`, `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/prompt/__init__.py`, `llmpebase/prompt/system_prompt.py` 添加 "Let's think step by step.",

`BaseZeroShotCoTPrompting_compare` 就是 Let's think step by step. 所以 `llmpebase/model/prompting/base.py` 不用添加新类. 需要修改 `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/model/__init__.py`, 给 prompts_factory 添加新数据集使用的 prompt, 主要设置 zeroshot_cot就可以

`/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/extractor/__init__.py` 添加 extractor, `/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/evaluator/__init__.py` 添加 evaluator

`/home/wuzongqian/anaconda/lib/python3.11/site-packages/llmpebase/pipeline.py` 不加载 trainset