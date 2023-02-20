<script>
    import {Cell as GridCell} from '@smui/layout-grid';
    import Select, {Option} from '@smui/select';
    import Button from '@smui/button';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text/index';

    const handleReportClick = (project, status) => {
        window.location = `/api/v1/report?project=${project}&status=${status}`;
    }

    let selectedProject = 'RD';
    let projects = [
        'RD',
        'ARZ',
        'FEB',
        'OFB',
        'FEP',
        'HTL',
        'RNDGEOM',
        'CMX',
        'RNDTEAM',
        'MS',
        'NTM',
        'RNDTP',
        'RNDBACKEND',
    ];

    let status = '';
</script>

<GridCell span={4}></GridCell>
<GridCell span={6}>
    <Select bind:value={selectedProject} label="Project">
        <Option value=""/>
        {#each projects as project}
            <Option value="{project}">{project}</Option>
        {/each}
    </Select>
    <Textfield bind:value={status} label="Label">
        <HelperText slot="helper">Status</HelperText>
    </Textfield>

    <Button on:click={() => handleReportClick(selectedProject, status)} variant="raised">Make magic!</Button>
</GridCell>
<GridCell span={2}></GridCell>