export const getIssuesEstimation = (selectedUser, numberOfDays, project, withoutDocumentations) => {
    return fetch('/api/v1/issues-estimation?' + new URLSearchParams({
        user: selectedUser,
        days: numberOfDays,
        project: project,
        withoutDocumentations: withoutDocumentations,
    }).toString())
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            return data;
        });
}

export const getIssuesPipeline = (project, numberOfDays, selectedUser = '') => {
    return fetch('/api/v1/issues-pipeline?' + new URLSearchParams({
        user: selectedUser,
        days: numberOfDays,
        project: project,
    }).toString())
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            return data;
        });
}