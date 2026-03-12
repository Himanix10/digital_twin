import { runModel, explainAI } from "../services/api"
import { useState } from "react"

import Sidebar from "../components/Sidebar"
import Header from "../components/Header"
import MetricCard from "../components/MetricCard"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts"

import "../styles/dashboard.css"

function Dashboard(){

const [result,setResult] = useState(null)
const [chartData,setChartData] = useState([])
const [explanation,setExplanation] = useState("")

const [model,setModel] = useState("Random Forest")
const [horizon,setHorizon] = useState(10)

const runPrediction = async()=>{

const sampleData={
data:[
{temperature:50,vibration:30,pressure:100},
{temperature:52,vibration:31,pressure:102},
{temperature:49,vibration:29,pressure:101},
{temperature:51,vibration:30,pressure:103},
{temperature:48,vibration:28,pressure:99},
{temperature:53,vibration:32,pressure:104},
{temperature:47,vibration:27,pressure:98}
],
sensors:["temperature","vibration"],
model:model,
horizon:horizon
}

try{

const response = await runModel(sampleData)

const data = response.data

setResult(data)

const chart = data.actual.map((value,index)=>({
index:index,
actual:value,
predicted:data.predicted[index]
}))

setChartData(chart)

}catch(err){

console.error(err)
alert("Backend error")

}

}

const generateExplanation = async()=>{

try{

const response = await explainAI({
health:result.health,
anomalies:result.anomalies.length,
noise:result.noise
})

setExplanation(response.data.explanation)

}catch{

alert("Explanation error")

}

}

return(

<div className="layout">

<Sidebar/>

<div className="main">

<Header/>

<div className="content">

<div className="controls">

<div>

<label>Model</label>

<select
value={model}
onChange={(e)=>setModel(e.target.value)}
>

<option>Linear Regression</option>
<option>Random Forest</option>
<option>LSTM</option>
<option>Autoencoder</option>

</select>

</div>

<div>

<label>Prediction Horizon</label>

<input
type="number"
value={horizon}
onChange={(e)=>setHorizon(e.target.value)}
min={1}
max={50}
/>

</div>

<button className="primaryBtn" onClick={runPrediction}>
Run Model
</button>

</div>

{result && (

<div className="metrics">

<MetricCard title="Health Score" value={result.health.toFixed(2)}/>

<MetricCard title="Anomalies" value={result.anomalies.length}/>

<MetricCard title="Noise" value={result.noise.toFixed(2)}/>

</div>

)}

{chartData.length>0 && (

<div className="chartArea">

<h2>System Prediction</h2>

<ResponsiveContainer width="100%" height={350}>

<LineChart data={chartData}>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="index"/>

<YAxis/>

<Tooltip/>

<Line
type="monotone"
dataKey="actual"
stroke="#3b82f6"
strokeWidth={3}
/>

<Line
type="monotone"
dataKey="predicted"
stroke="#ef4444"
strokeWidth={3}
/>

</LineChart>

</ResponsiveContainer>

</div>

)}

{result && (

<div className="actions">

<button
className="primaryBtn"
onClick={generateExplanation}
>

Generate AI Explanation

</button>

</div>

)}

{explanation && (

<div className="explanation">

<h2>AI Explanation</h2>

<pre>{explanation}</pre>

</div>

)}

</div>

</div>

</div>

)

}

export default Dashboard