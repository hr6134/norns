<script>
    import LayoutGrid, {Cell as GridCell} from '@smui/layout-grid';
    import Tab, {Label} from '@smui/tab';
    import TabBar from '@smui/tab-bar';

    import EstimationPage from "./EstimationPage.svelte";
    import PipelinePage from "./PipelinePage.svelte";
    import Reports from "./Reports.svelte";
    import DetailedEstimationPage from "./DetailedEstimationPage.svelte";

    let active = 'Detailed Estimation';
</script>

<LayoutGrid>
    <GridCell span={12}>
        <TabBar tabs={['Detailed Estimation', 'Estimation', 'Pipeline', 'Reports']} let:tab bind:active>
            <Tab {tab}>
                <Label>{tab}</Label>
            </Tab>
        </TabBar>
    </GridCell>

    {#if active == 'Detailed Estimation'}
        <DetailedEstimationPage/>
    {:else if active == 'Estimation'}
        <EstimationPage/>
    {:else if active == 'Pipeline'}
        <PipelinePage/>
    {:else if active == 'Reports'}
        <Reports/>
    {/if}

</LayoutGrid>