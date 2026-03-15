import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { useModelContext } from "../context/ModelContext";
import { saveAs } from "file-saver";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import "../styles/dashboard.css";

function Reports() {
  
  const { lastRun } = useModelContext();

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(lastRun, null, 2)], {
      type: "application/json",
    });
    saveAs(blob, "digital_twin_report.json");
  };

  const downloadCSV = () => {
    const csv = `Model,${lastRun.model}
Sensors,${lastRun.sensors.join(" | ")}
Health Score,${lastRun.health}
Anomalies,${lastRun.anomalies}
Timestamp,${new Date().toLocaleString()}
`;
    const blob = new Blob([csv], { type: "text/csv" });
    saveAs(blob, "digital_twin_report.csv");
  };

  const downloadPDF = async () => {
    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text("Hybrid Digital Twin Analysis Report", 20, 20);

    doc.setFontSize(12);
    doc.text(`Model Used: ${lastRun.model}`,             20, 40);
    doc.text(`Sensors: ${lastRun.sensors.join(", ")}`,   20, 50);
    doc.text(`Health Score: ${lastRun.health}`,          20, 60);
    doc.text(`Anomalies Detected: ${lastRun.anomalies}`, 20, 70);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 80);

    if (lastRun.actual?.length) {
      const avg = lastRun.actual.reduce((a, b) => a + b, 0) / lastRun.actual.length;
      const max = Math.max(...lastRun.actual);
      const min = Math.min(...lastRun.actual);

      doc.text("Sensor Data Summary:", 20, 100);
      doc.text(`Average Sensor Value: ${avg.toFixed(2)}`, 20, 110);
      doc.text(`Max Sensor Value: ${max.toFixed(2)}`,     20, 120);
      doc.text(`Min Sensor Value: ${min.toFixed(2)}`,     20, 130);
    }

    const chart = document.getElementById("predictionChart");
    if (chart) {
      const canvas = await html2canvas(chart);
      const img = canvas.toDataURL("image/png");
      doc.addPage();
      doc.text("Prediction Chart", 20, 20);
      doc.addImage(img, "PNG", 15, 30, 180, 100);
    }

    doc.save("digital_twin_report.pdf");
  };

  return (
    <div className="layout">
      <Sidebar />

      <div className="main">
        <Header />

        <div className="content">

          <div className="pageHeader">
            <h1>Reports</h1>
            <p>Download analytics and export session data</p>
          </div>

          {!lastRun && (
            <div className="emptyState">
              <p>Run a model in the dashboard to generate a report.</p>
            </div>
          )}

          {lastRun && (
            <div className="chartArea">
              <h2>Export Analysis Report</h2>

              <div className="metrics">

                <div className="metricCard">
                  <h4>Download PDF</h4>
                  <p style={{ fontSize: 12, marginBottom: 12 }}>
                    Full report with chart screenshot
                  </p>
                  <button className="primaryBtn" onClick={downloadPDF}>
                    Export PDF
                  </button>
                </div>

                <div className="metricCard">
                  <h4>Download CSV</h4>
                  <p style={{ fontSize: 12, marginBottom: 12 }}>
                    Summary metrics in spreadsheet format
                  </p>
                  <button className="primaryBtn" onClick={downloadCSV}>
                    Export CSV
                  </button>
                </div>

                <div className="metricCard">
                  <h4>Download JSON</h4>
                  <p style={{ fontSize: 12, marginBottom: 12 }}>
                    Full raw data including sensor arrays
                  </p>
                  <button className="primaryBtn" onClick={downloadJSON}>
                    Export JSON
                  </button>
                </div>

              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default Reports;