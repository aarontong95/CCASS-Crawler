url = 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx'
image_save_path = 'static/output.png'

shareholding_columns = [
    {
            "field": "date",
            "title": "Date",
            "sortable": True
        },
        {
            "field": "participant_id",
            "title": "Participant ID",
            "sortable": True
        },
        {
            "field": "percent",
            "title": "Percentage of Shares",
            "sortable": True
        }
]

transaction_columns = [
    {
            "field": "date",
            "title": "Date",
            "sortable": True
        },
        {
            "field": "exchange_shares",
            "title": "Exchange Shares(%)",
            "sortable": True
        },
        {
            "field": "participant_id_BUY",
            "title": "Participant ID BUY",
            "sortable": True
        },
        {
            "field": "participant_id_SELL",
            "title": "Participant ID SELL",
            "sortable": True
        }
]