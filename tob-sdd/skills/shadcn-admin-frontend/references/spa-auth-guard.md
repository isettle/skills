# SPA JWT 登录守卫竞态 recipe

## 症状

登录接口成功、`setToken(localStorage)` + `navigate("/dashboard")`，页面却立刻被弹回 /login。

## 根因机制

AuthProvider 用 `const hasToken = !!getToken()`（渲染时快照）作 useQuery 的 enabled 条件；setToken 只写 localStorage 不触发重渲染 → 守卫渲染时 hasToken 仍 false → query 未 enable → `me=null && loading=false` → `<Navigate to="/login">`。

## 修法（验证过的模式）

1. AuthProvider 持 state：`const [token, setTokenState] = useState(() => getToken())`；query `enabled: !!token`。
2. context 暴露 `applyToken(t)`：写 localStorage + setState（触发重渲染 → query enable）。
3. loading 语义＝`!!token && !query.data`——不能用 `query.isPending`（未 enable 时恒 false，守卫会误判为「无登录态」）。
4. `logout()` 收敛进 context：clearToken + setState(null) + `queryClient.removeQueries({queryKey:["auth","me"]})`；页面组件不直接碰 localStorage。
5. 登录 onSuccess：`applyToken(result.token); navigate("/workbench", {replace:true})`。守卫在 me 未就绪期间显示「正在加载…」，就绪后自然放行。

## 验证清单

- 登录跳转用四条路径各验一次：后端直连、代理 IPv4（127.0.0.1）、代理 IPv6（[::1]）、localhost——vite 监听协议栈差异会只在部分路径暴露。
- 修完权限/角色类 bug 后提醒用户清 localStorage 旧 token——旧 token 签发的角色会造成「修了还是不对」的假象。
