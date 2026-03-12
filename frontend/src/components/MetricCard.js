import "../styles/dashboard.css";

function MetricCard({title,value}){

  return(

    <div className="metricCard">

      <h4>{title}</h4>

      <h2>{value}</h2>

    </div>

  )

}

export default MetricCard