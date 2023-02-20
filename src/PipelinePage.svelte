<script>
    import Button from '@smui/button';
    import {Cell as GridCell} from '@smui/layout-grid';
    import Slider from '@smui/slider';
    import Select, {Option} from '@smui/select';
    import Bar from "svelte-chartjs/src/Bar.svelte";

    import {getIssuesPipeline} from "./issues";
    import {buildPipelinePlot} from "./utils";
    import {getUsers} from "./users";

    let numberOfDays = 14;
    let selectedUser = '';
    let selectedProject = 'runtime-base';
    let projects = [
        'runtime-base',
        'runtime-product',
        'indexer',
        'runtime-nlp',
    ];

    let users = [];

    $: getUsers(selectedProject).then(data => {
        selectedUser = '';
        users = data;
    })

    let issuesData = {
        labels: [],
        datasets: []
    };

    const filter = () => {
        getIssuesPipeline(selectedProject, numberOfDays, selectedUser).then((data) => {
            console.log(data);
            issuesData = buildPipelinePlot(data);
        });
    }

    let options = {
        responsive: true,
        scales: {
            xAxes: [
                {
                    barPercentage: 1,
                    gridLines: {
                        display: true,
                        color: "rgba(0, 0, 0, 0.1)"
                    }
                }
            ],
            yAxes: [
                {
                    gridLines: {
                        display: true,
                        color: "rgba(0, 0, 0, 0.1)"
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }
            ]
        }
    }
</script>

<GridCell span={4}>
    <Slider
            bind:value={numberOfDays}
            min={0}
            max={91}
            step={7}
            discrete
            tickMarks
            input$aria-label="Tick mark slider"
    />
</GridCell>
<GridCell span={6}>
    <Select bind:value={selectedProject} label="Project">
        <Option value=""/>
        {#each projects as project}
            <Option value="{project}">{project}</Option>
        {/each}
    </Select>
    <Select bind:value={selectedUser} label="User">
        <Option value=""/>
        {#each users as user}
            <Option value="{user.id}">{user.name}</Option>
        {/each}
    </Select>

    <Button on:click={filter} variant="raised">Filter</Button>
</GridCell>
<GridCell span={2}></GridCell>

<GridCell span={12}>
    <Bar data={issuesData} {options}/>
</GridCell>