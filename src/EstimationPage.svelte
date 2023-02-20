<script>
    import Button from '@smui/button';
    import {Cell as GridCell} from '@smui/layout-grid';
    import Slider from '@smui/slider';
    import Select, {Option} from '@smui/select';
    import HorizontalBar from "svelte-chartjs/src/HorizontalBar.svelte";

    import StatsTable from "./StatsTable.svelte";
    import ShortIssuesTable from "./ShortIssuesTable.svelte";

    import {getUsers} from "./users.js";
    import {getIssuesEstimation} from "./issues.js";
    import {calculateStats, buildEstimationsPlot} from "./utils.js";

    let selectedProject = 'runtime-base';
    let projects = [
        'runtime-base',
        'runtime-product',
        'indexer',
        'runtime-nlp',
    ];

    let rows = [];
    let selectedUser = '';
    let numberOfDays = 14;

    let totalDelay = 0;
    let avgDelay = 0;

    let issuesData = {
        labels: [],
        datasets: []
    };

    let users = [];

    $: getUsers(selectedProject).then(data => {
        selectedUser = '';
        users = data;
    })

    const filter = () => {
        getIssuesEstimation(selectedUser, numberOfDays, selectedProject).then((data) => {
            rows = data;

            let stats = calculateStats(data);
            avgDelay = stats.avgDelay;
            totalDelay = stats.totalDelay;
            issuesData = buildEstimationsPlot(data);
        })
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

<GridCell span={6}>
    <ShortIssuesTable {rows}/>
</GridCell>

<GridCell span={6}>
    <GridCell span={12}>
        <StatsTable {totalDelay} {avgDelay}/>
    </GridCell>
    <GridCell span={12}>
        <HorizontalBar data={issuesData} {options}/>
    </GridCell>
</GridCell>