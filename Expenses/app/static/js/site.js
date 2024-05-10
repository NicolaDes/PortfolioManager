// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

function expensesPieChart(pId) {
    var year = document.getElementById("yearSelect").value;
    var month = document.getElementById("monthSelect").value;
    var monthDesc = "All";
    if (month != -1) {
        monthDesc = "" + month;
    }
    $.getJSON("/Analytics/CategoriesYearly/"+pId+"?year=" + year + "&month=" + month + "&type=Outcome", function (data) {

        let serie = [];
        for (let i in data) {
            serie.push({
                name: i,
                y: Math.abs(data[i])
            });
        }

        Highcharts.chart('expensesPieChartContainer', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Expenses By Category for year/month:' + year + '/' + monthDesc,
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
                    }
                }
            },
            series: [{
                name: 'Categories',
                colorByPoint: true,
                data: serie
            }]
        });
    });
};

function expensesLabelsPieChart(pId) {
    var year = document.getElementById("yearSelect").value;
    var month = document.getElementById("monthSelect").value;
    var monthDesc = "All";
    if (month != -1) {
        monthDesc = "" + month;
    }
    console.log("Waglio!");
    $.getJSON("/Analytics/LabelsYearly/" + pId + "?year=" + year + "&month=" + month + "&type=Outcome", function (data) {

        let serie = [];
        for (let i in data) {
            serie.push({
                name: i,
                y: Math.abs(data[i])
            });
        }

        console.log(serie);

        Highcharts.chart('expensesLabelsPieChartContainer', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Expenses by Labels for year/month:' + year + '/' + monthDesc,
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
                    }
                }
            },
            series: [{
                name: 'Categories',
                colorByPoint: true,
                data: serie
            }]
        });
    });
};

function expensesColumnChart(pId) {
    var year = document.getElementById("yearSelect").value;
    $.getJSON("/Analytics/CategoriesByMonthYearly/"+pId+"?year=" + year + "&type=Outcome", function (dta) {

        let serie = [];
        for (let i in dta) {
            serie.push({
                name: i,
                data: dta[i]
            });
        }

        Highcharts.chart('expensesColumnChartContainer', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Expenses for year ' + year,
            },
            yAxis: {
                title: {
                    text: "Eur"
                }
            },
            xAxis: {
                categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                title: {
                    text: "Months"
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: false
                    }
                }
            },
            series: serie
        });
    });
};

function yearlyIncomeExpensesChart(pId) {
    var year = document.getElementById("yearSelect").value;
    $.getJSON("/Analytics/YearlyIncomExpenses/" + pId + "?year=" + year + "&type=Outcome", function (dta) {
        let serie = [];
        for (let i in dta) {
            serie.push({
                name: i,
                y: dta[i]
            });
        }

        console.log("Ciaone: ", serie)

        Highcharts.chart('yearlyIncomeExpenses', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Income/Expenses' + year,
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
                    }
                }
            },
            series: [{
                name: 'Type',
                colorByPoint: true,
                data: serie
            }]
        });
    });
}

function incomePieChart(pId) {
    var year = document.getElementById("yearSelect").value;
    var month = document.getElementById("monthSelect").value;
    var monthDesc = "All";
    if (month != -1) {
        monthDesc = "" + month;
    }
    $.getJSON("/Analytics/CategoriesYearly/" + pId + "?year=" + year + "&month=" + month + "&type=Income", function (data) {

        let serie = [];
        for (let i in data) {
            serie.push({
                name: i,
                y: Math.abs(data[i])
            });
        }

        Highcharts.chart('incomePieChartContainer', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Income for year/month:' + year + '/' + monthDesc,
                align: 'left'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
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
                    }
                }
            },
            series: [{
                name: 'Categories',
                colorByPoint: true,
                data: serie
            }]
        });
    });
};

function incomeColumnChart(pId) {
    var year = document.getElementById("yearSelect").value;
    $.getJSON("/Analytics/CategoriesByMonthYearly/" + pId + "?year=" + year + "&type=Income", function (dta) {

        let serie = [];
        for (let i in dta) {
            serie.push({
                name: i,
                data: dta[i]
            });
        }

        Highcharts.chart('incomeColumnChartContainer', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Income for year ' + year,
            },
            yAxis: {
                title: {
                    text: "Eur"
                }
            },
            xAxis: {
                categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                title: {
                    text: "Months"
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: false
                    }
                }
            },
            series: serie
        });
    });
};

function incomeLineChart(pId) {
    var year = document.getElementById("yearSelect").value;
    $.getJSON("/Analytics/IncomeCategoriesByMonthYearly/" + pId + "?year=" + year, function (dta) {

        let serie = [];
        let cashFlow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        let cumulativeCashFlow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

        serie.push({
            name: "Salary",
            type: 'column',
            data: dta["Salary"],
            color: '#b2e061'
        });

        serie.push({
            name: "Outcome",
            type: 'column',
            data: dta["Outcome"],
            color: '#fd7f6f'
        });

        for (let i = 0; i < 12; ++i) {
            cashFlow[i] = dta["Salary"][i] + dta["Outcome"][i];
            if (i == 0) {
                cumulativeCashFlow[0] = cashFlow[0];
            }
            else {
                cumulativeCashFlow[i] = cumulativeCashFlow[i - 1] + cashFlow[i];
            }
        }

        serie.push({
            name: 'CashFlow',
            type: 'spline',
            color: 'blue',
            data: cashFlow
        });

        serie.push({
            name: 'Cumulative Cash Flow',
            type: 'area',
            color: '#ffb55a',
            data: cumulativeCashFlow
        });

        Highcharts.chart('incomeLineChartContainer', {
            title: {
                text: 'Income for year ' + year,
            },
            yAxis: {
                title: {
                    text: "Eur"
                }
            },
            xAxis: {
                categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                title: {
                    text: "Months"
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: false
                    }
                }
            },
            series: serie
        });
    });
};

function paintPieCharts(pId) {
    expensesPieChart(pId);
    expensesLabelsPieChart(pId);
    //incomePieChart(pId);
};

function paintColumnCharts(pId) {
    expensesColumnChart(pId);
    //incomeColumnChart(pId);
};

function paintAllCharts(pId) {
    paintPieCharts(pId);
    yearlyIncomeExpensesChart(pId);
    paintColumnCharts(pId);
    incomeLineChart(pId);
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


function createAssetTable() {
    // Setup - add a text input to each footer cell
    var cryptoTable = $('#cryptoAssetsTable').DataTable({
        orderCellsTop: true,
        fixedHeader: true
    });
    var nftsTable = $('#nftsAssetsTable').DataTable({
        orderCellsTop: true,
        fixedHeader: true
    });
    var stocksTable = $('#stocksAssetsTable').DataTable({
        orderCellsTop: true,
        fixedHeader: true
    });
}