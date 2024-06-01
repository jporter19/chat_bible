#%%
# This is a RunnableLambda
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one)

runnable.invoke(1) # returns 2
runnable.batch([1, 2, 3]) # returns [2, 3, 4]

# Async is supported by default by delegating to the sync implementation
await runnable.ainvoke(1) # returns 2
await runnable.abatch([1, 2, 3]) # returns [2, 3, 4]


# Alternatively, can provide both synd and sync implementations
async def add_one_async(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one, afunc=add_one_async)
runnable.invoke(1) # Uses add_one
await runnable.ainvoke(1) # Uses add_one_async