<script>
    import DataTable, {Head, Body, Row, Cell} from '@smui/data-table';

    export let rows;

    let sort = 'id';
    let sortDirection = 'ascending';

    const handleSort = () => {
        rows.sort((a, b) => {
            const [aVal, bVal] = [a[sort], b[sort]][
                sortDirection === 'ascending' ? 'slice' : 'reverse'
                ]();
            if (typeof aVal === 'string') {
                return aVal.localeCompare(bVal);
            }
            return aVal - bVal;
        });
        rows = rows;
    }

    const getColor = (row) => {
        if (!row.epic && !row.techcom_status && !row.techcom_est) {
            return 'background-color: rgba(255, 0, 134, 0.4);';
        }

        if (row.estimation === null) {
            return 'background-color: rgba(255, 134, 159, 0.4);';
        }

        if (row.estimation && row.estimation < row.timespent) {
            return 'background-color: rgba(255, 134, 0, 0.4);';
        }

        return ''
    }

    $: statuses = () => {
        let statuses = {};
        for (let row of rows) {
            if (row.status in statuses) {
                statuses[row.status] += 1;
            } else {
                statuses[row.status] = 1;
            }
        }

        let result = '';
        for (let key of Object.keys(statuses)) {
            result += `${key}: ${statuses[key]}  |  `;
        }
        return result;
    }

    let currentHover = '';
</script>

<div style="margin-bottom: 5px">
    <span>Rows: {rows.length}</span>
</div>
<div style="margin-bottom: 5px">
    <span>{statuses()}</span>
</div>

<DataTable
        style="width: 100%;"
        sortable
        bind:sort
        bind:sortDirection
        on:MDCDataTable:sorted={handleSort}
        stickyHeader
>
    <Head>
        <Row>
            <Cell columnId="key">Key</Cell>
            <Cell columnId="timespent">Timespent</Cell>
            <Cell columnId="review_total">Review</Cell>
            <Cell columnId="ready_for_testing_total">RfT</Cell>
            <Cell columnId="testing_total">Testing</Cell>
            <Cell columnId="release_testing_total">R Testing</Cell>
            <Cell columnId="development_done_total">DD</Cell>
            <Cell columnId="ready_to_deploy_total">RfD</Cell>
            <Cell columnId="estimation">Estimation</Cell>
            <Cell columnId="status">Status</Cell>
            <Cell columnId="labels">Labels</Cell>
            <Cell columnId="epic">Epic</Cell>
            <Cell columnId="techcom_status">Tech Com</Cell>
            <Cell columnId="techcom_est">T-Shirt</Cell>
            <Cell columnId="duedate">Due</Cell>
            <Cell columnId="assigned">Assigned</Cell>
        </Row>
    </Head>
    <Body>
    {#each rows as row}
        <Row style="{getColor(row)}">
            <Cell>
                <a href="https://jit.o3.ru/browse/{row.issue_key}"
                   target="_blank"
                   on:mouseover={() => currentHover = row.issue_key}
                   on:mouseleave={() => currentHover = ''}
                >
                    {row.issue_key}
                </a>
                {#if currentHover === row.issue_key}
                    <div class="tooltip"

                    >
                        {row.summary}
                    </div>
                {/if}
            </Cell>
            <Cell>{row.timespent?.toFixed(2)}</Cell>
            <Cell>{row.review_total?.toFixed(2)}</Cell>
            <Cell>{row.ready_for_testing_total?.toFixed(2)}</Cell>
            <Cell>{row.testing_total?.toFixed(2)}</Cell>
            <Cell>{row.release_testing_total?.toFixed(2)}</Cell>
            <Cell>{row.development_done_total?.toFixed(2)}</Cell>
            <Cell>{row.ready_to_deploy_total?.toFixed(2)}</Cell>
            <Cell>{row.estimation?.toFixed(2)}</Cell>
            <Cell>{row.status}</Cell>
            <Cell>{row.labels}</Cell>
            <Cell>
                {#if row.epic}
                    <a href="https://jit.o3.ru/browse/{row.epic}"
                       target="_blank"
                    >
                        {row.epic}
                    </a>
                {/if}
            </Cell>
            <Cell>{row.techcom_status}</Cell>
            <Cell>{row.techcom_est}</Cell>
            <Cell>{row.duedate || ''}</Cell>
            <Cell>{row.assigned}</Cell>
        </Row>
    {/each}
    </Body>
</DataTable>

<style>
    .cell-with-tooltip {
        position: relative;
    }

    .tooltip {
        width: 400px;
        white-space: break-spaces;
        position: absolute;
        background-color: white;
        padding: 5px 10px;
        border: 1px solid;
        border-radius: 5px;
    }
</style>