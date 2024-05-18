
// Serie should be [{name: "label1", y: data1}, ..., {name: "labelN", y: dataN}
function pieChart(serie, container, pieName, title)
{
    Highcharts.chart(container, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: title,
            align: 'left'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y:.1f} €</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                },
                showInLegend: true
            }
        },
        series: [{
            name: pieName,
            colorByPoint: true,
            data: serie
        }],
        credits: {
            enabled: false
        }
    });
}

// serie := [{name: 'Cat1', data: [1, 4, 31, 23, ..., 32]}]
// categories := ['Jan', 'Feb', ..., 'Dec']
function columnStackChart(serie, categories, container, title, yAxisLabel) {
    console.log(serie);
    console.log(categories);

    const chartData = {
        chart: {
            type: 'column',
        },
        title: {
            text: title,
            align: 'left'
        },
        xAxis: {
            categories: categories,
        },
        yAxis: {
            title: {
                text: yAxisLabel,
            },
            stackLabels: {
                enabled: false
            }
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled : false
                }
            }
        },
        series: serie
    };

    Highcharts.chart(container, chartData);
}


// Remove the formatting to get integer data for summation
function intVal(i) {
    ret = typeof i === 'string' ? i.replace(/[\$€,]/g, '') * 1 : typeof i === 'number' ? i : 0;
    return Number(ret);
};

function floatVal(f) {
    ret = typeof f === 'string' ? f.replace(/[\$€,]/g, '') * 1.0 : typeof f === 'number' ? f : 0.0;
    return Number(ret);
}

function createTable() {
    // Setup - add a text input to each footer cell
    $('#transactionsTable thead tr')
        .clone(true)
        .addClass('filters')
        .appendTo('#transactionsTable thead');
    var sizes = [1, 4, 8, 40, 8, 2, 2, 4, 4];
    var placeholders = ["Id", "Value", "Label", "Description", "Date", "Currency", "Percentage To Exclude", "Type", "Class"];
    var table = $('#transactionsTable').DataTable({
        footerCallback: function (row, data, start, end, display) {
            var api = this.api();
            total = api
                .column(1, {
                    page: 'all',
                    filter: 'applied'
                })
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            $(api.column(1).footer()).html(total.toFixed(0) + ' €');
        },
        orderCellsTop: true,
        fixedHeader: true,
        initComplete: function () {
            var api = this.api();
            // For each column
            api
                .columns()
                .eq(0)
                .each(function (colIdx) {
                    // Set the header cell to contain the input element
                    var cell = $('.filters th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    if (colIdx < 9) {
                        $(cell).html('<input type="text" size=' + sizes[colIdx] + ' placeholder="' + placeholders[colIdx] + '" />');

                        if ($(api.column(colIdx).header()).index() >= 0) {
                            $(cell).html('<input type="text" size=' + sizes[colIdx] + ' placeholder="' + placeholders[colIdx] + '"/>');
                        }

                        // On every keypress in this input
                        $(
                            'input',
                            $('.filters th').eq($(api.column(colIdx).header()).index())
                        )
                            .off('keyup change')
                            .on('change', function (e) {
                                // Get the search value
                                $(this).attr('title', $(this).val());
                                var regexr = '({search})'; //$(this).parents('th').find('select').val();
                                var cursorPosition = this.selectionStart;
                                // Search the column for that value
                                api
                                    .column(colIdx)
                                    .search(
                                        this.value != '' ?
                                            regexr.replace('{search}', '(((' + this.value + ')))') :
                                            '',
                                        this.value != '',
                                        this.value == ''
                                    )
                                    .draw();
                            })
                            .on('keyup', function (e) {
                                e.stopPropagation();
                                $(this).trigger('change');
                                $(this)
                                    .focus()[0]
                                    .setSelectionRange(cursorPosition, cursorPosition);
                            });
                    }
                });
        },
    });
}
