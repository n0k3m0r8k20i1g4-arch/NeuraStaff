from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn, json, random, datetime, base64

app = FastAPI()
DATA_FILE="data.json"

try:
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        db=json.load(f)
except:
    db={"tasks":[],"logs":[],"agents":{},"performance":{}}

# AI社員リスト
agents = {
    "教育":["教育1","教育2","教育3"],
    "実行":["実行1","実行2","実行3"],
    "AI構築":["AI1","AI2","AI3","AI4","AI5","AI6","AI7","AI8","AI9","AI10"],
    "監視":["監視"],
    "データ管理":["データ生成1","データ生成2","データ生成3"],
    "活用":["活用1","活用2","活用3"],
    "チャット":["チャット1","チャット2","チャット3","チャット4","チャット5"]
}

# 性能処理関数
def perform(agent, performance, text):
    # 基本返信
    reply=f"{agent} が {performance} を実行: {text}"
    # 簡易学習ランダム
    if random.random()<0.4:
        db["agents"][agent]=db["agents"].get(agent,0)+1
        reply+=f" ✅ 学習済み({db['agents'][agent]}回)"
    # 性能履歴
    db["performance"].setdefault(agent,{})[performance]=db["performance"][agent].get(performance,0)+1
    # Base64変換例
    if performance=="Base64変換":
        reply=f"Base64: {base64.b64encode(text.encode()).decode()}"
    # タスク保存
    db["tasks"].append({"agent":agent,"performance":performance,"task":text,"done":False})
    db["logs"].append({"agent":agent,"performance":performance,"text":text,"time":str(datetime.datetime.now())})
    save_db()
    return reply

def save_db():
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(db,f,ensure_ascii=False,indent=2)

@app.post("/process")
async def process(request:Request):
    data = await request.json()
    agent = data.get("agent","不明")
    performance = data.get("performance","通常処理")
    text = data.get("text","")
    if agent not in agents: agent="チャット"
    reply = perform(agent,performance,text)
    return JSONResponse({"reply":reply})

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
