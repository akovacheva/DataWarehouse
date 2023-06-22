from django.shortcuts import render
from etl_tables_view.functions.connection import get_connection
import json
from django.http import JsonResponse


# Create your views here.

TARGET_SOURCE_MAPPING = {
    "DimParty":[
        "Customer",
        "Region",
        "Country"
    ],
        "DimContract":[
        "Customer",
        "Contract",
        "Product"
    ],
    "FactContract":[
        "Contract",
        "ContractBalances"
    ]
}

TARGET_TABLES = ['DimParty', 'DimContract','FactContract']


def test_func(request):
    context = {}
    return render(request, 'base.html', context=context)


def users(request, table_name):

    # start = int(request.GET.get('start', 0))
    # length = int(request.GET.get('length', 10))
    # order_by_col = request.GET.get('order_by_col', 'FirstName')

    target_connection = get_connection('localhost', 'target_db').cursor()
    source_connection = get_connection('localhost', 'source_db').cursor()

    sources = TARGET_SOURCE_MAPPING[table_name]
    
    target_table = {}
    target_table['name'] = table_name
    # target_table['rows'] = target_connection.execute(f'SELECT * FROM dbo.{table_name} ORDER BY {order_by_col} OFFSET {start} ROWS FETCH NEXT {length} ROWS ONLY').fetchall()
    target_table['rows'] = target_connection.execute(f'SELECT * FROM dbo.{table_name}').fetchall()
    target_table['columns'] = [col[0] for col in target_connection.description]

    source_tables={}

    for source in sources:
        source_table = {}
        source_table['name'] = source
        # source_table['rows'] = source_connection.execute(f'SELECT * FROM dbo.{source} ORDER BY {order_by_col} OFFSET {start} ROWS FETCH NEXT {length} ROWS ONLY').fetchall()
        source_table['rows'] = source_connection.execute(f'SELECT * FROM dbo.{source}').fetchall()
        source_table['columns'] = [col[0] for col in source_connection.description]

        source_tables[source] = source_table


    context = {
        'target_table': target_table,
        'source_tables': source_tables
    }

    target_connection.close()

    if table_name == 'DimParty':
        return render(request, 'user.html', context=context)
    if table_name == 'DimContract':
        return render(request, 'contract.html', context=context)
    if table_name == 'FactContract':
        return render(request, 'FactContract.html', context=context)


# http://127.0.0.1:8000/etl_web/datable/DimParty/?length=100&start=60



def get_data(table_name, start, length, order_by, order_direction, search):
    cursor = get_connection('localhost','target_db').cursor() if table_name in TARGET_TABLES else get_connection('localhost','source_db').cursor()

    columns_query = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
    columns = [col[3] for col in cursor.execute(columns_query).fetchall()]
    records_total = cursor.execute(f'SELECT COUNT(*) FROM dbo.{table_name}').fetchone()[0]

    if search:
        conditions = ' OR '.join(f"{column} LIKE '%{search}%'" for column in columns)
        query = f"SELECT * FROM dbo.{table_name} WHERE {conditions}"
        count_query = f"SELECT COUNT(*) FROM dbo.{table_name} WHERE {conditions}"
        records_filtered = cursor.execute(count_query).fetchone()[0]
    else:
        query = f"SELECT * FROM dbo.{table_name}"
        records_filtered = records_total

    query += f" ORDER BY {columns[int(order_by)]} {order_direction} OFFSET {int(start)} ROWS FETCH NEXT {int(length)} ROWS ONLY"
    data = [list(row) for row in cursor.execute(query).fetchall()]

    return data, records_total, records_filtered


def datatable(request, table_name):
    start = request.GET.get('start', 0)
    length = request.GET.get('length', 30)
    order_by = request.GET.get('order[0][column]', 0)
    order_direction = request.GET.get('order[0][dir]', 'asc')
    search = request.GET.get('search[value]', '')
    draw = int(request.GET.get('draw', 1))

    data, records_total, records_filtered = get_data(table_name, start, length, order_by, order_direction, search)

    return JsonResponse({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data
    })


