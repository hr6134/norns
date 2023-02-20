export const getUsers = (project) => {
    return fetch('/api/v1/get-users?' + new URLSearchParams({project: project}).toString())
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let users = [];
            for (let k in data) {
                users = [...users, {
                    id: k,
                    name: data[k],
                }];
            }

            return users;
        });
}