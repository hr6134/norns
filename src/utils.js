export const calculateStats = (data) => {
    let totalDelay = 0;
    let avgDelay = 0;

    const timespents = data.map(e => e.timespent);
    const estimations = data.map(e => e.estimation);

    totalDelay = timespents.reduce((a, b) => a + b, 0) -
        estimations.reduce((a, b) => a + b, 0);

    avgDelay = 0;
    for (let t in timespents) {
        if (estimations[t]) {
            avgDelay += timespents[t] - estimations[t];
        } else {
            avgDelay += timespents[t];
        }
    }
    avgDelay /= timespents.length;

    return {avgDelay, totalDelay};
}

export const buildEstimationsPlot = (data) => {
     let issuesData = {
        labels: [],
        datasets: []
    };

    issuesData.datasets = [];
    issuesData.labels = data.map(e => e.issue_key);

    issuesData.datasets.push({
        label: "timespent",
        data: data.map(e => e.timespent),
        backgroundColor: new Array(data.length).fill("rgba(255, 134, 159, 0.4)"),
        borderWidth: 2,
        borderColor: new Array(data.length).fill("rgba(255, 134, 159, 1)"),
    })

    issuesData.datasets.push({
        label: "Estimation",
        data: data.map(e => e.estimation),
        backgroundColor: new Array(data.length).fill("rgba(134, 255, 159, 0.4)"),
        borderWidth: 2,
        borderColor: new Array(data.length).fill("rgba(134, 255, 159, 1)"),
    })

    return issuesData;
}

export const buildPipelinePlot = (data) => {
     let issuesData = {
        labels: [],
        datasets: []
    };

    issuesData.datasets = [];
    issuesData.labels = Object.keys(data);

    let bgdColors = new Array(Object.keys(data).length).fill("rgba(204, 255, 255, 0.5)");
    bgdColors[findBiggestValue(Object.values(data), 1)] = "rgba(255, 51, 0, 0.5)";
    bgdColors[findBiggestValue(Object.values(data), 2)] = "rgba(255, 204, 102, 0.5)";
    bgdColors[findBiggestValue(Object.values(data), 3)] = "rgba(255, 255, 153, 0.5)";

    issuesData.datasets.push({
        label: "Timespent",
        data: Object.values(data),
        backgroundColor: bgdColors,
        borderWidth: 2,
        borderColor: new Array(Object.keys(data).length).fill("rgba(100, 100, 100, 0.4)"),
    })

    return issuesData;
}

const findBiggestValue = (values, pos) => {
    if (values.length < pos) return -1;

    return values.indexOf(values.map(e => parseFloat(e)).sort((a, b) => a - b)[values.length - pos]);
}