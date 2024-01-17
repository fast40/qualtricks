const javascriptCodeElement = document.getElementById("javascript");
const htmlCodeElement = document.getElementById("html");

const datasetNameSelector = document.querySelector("select[name=dataset_name]");
const orderingSelector = document.querySelector("select[name=ordering]");

function generateCode() {
    javascriptCodeElement.textContent = generateJavascript(datasetNameSelector.value, orderingSelector.value);
    htmlCodeElement.textContent = generateHTML(datasetNameSelector.value, orderingSelector.value);

    javascriptCodeElement.parentElement.style.display = "initial";
}

function generateJavascript(dataset_name, ordering) {
    return `const embeddedDataField = "Video" + String("\${lm://CurrentLoopNumber}");
const xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        Qualtrics.SurveyEngine.setEmbeddedData(embeddedDataField, xhttp.responseText);
    }
};
xhttp.open("GET", "http://localhost/get_url?dataset=${dataset_name}&ordering=${ordering}&response=\${e://Field/ResponseID}&loop_number=\${lm://CurrentLoopNumber}", true);
xhttp.send();`;
}

function generateHTML(dataset_name, ordering) {
    return `<video class="inserted-video" style="width: 100%;" controls playsinline>
<source id="video-source" src="http://localhost/get_url?dataset=${dataset_name}&ordering=${ordering}&response=\${e://Field/ResponseID}&loop_number=\${lm://CurrentLoopNumber}" type="video/mp4">
Your browser does not support the video tag.
</video>`;
}
