<script>
    import DataTable, {Head, Body, Row, Cell} from '@smui/data-table';

    export let totalDelay;
    export let avgDelay;
</script>


<DataTable style="width: 100%;">
    <Head>
        <Row>
            <Cell>Total timespent</Cell>
            <Cell>Avg delay</Cell>
        </Row>
    </Head>
    <Body>
    <Row>
        <Cell>{totalDelay}</Cell>
        <Cell>{avgDelay}</Cell>
    </Row>
    </Body>
</DataTable>