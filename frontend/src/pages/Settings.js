import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

function Settings(){

return(

<div className="layout">

<Sidebar/>

<div className="main">

<Header/>

<div className="content">

<h1>Settings</h1>

<p>System configuration options.</p>

</div>

</div>

</div>

)

}

export default Settings