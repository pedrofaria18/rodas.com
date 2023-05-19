GET_NEW_DOCS = "SELECT url_hash," \
                "    html_hash," \
                "    html," \
                "    id," \
                "    last_processing_data" \
                " FROM html_document" \
                " WHERE last_processing_data is null" \
                " AND is_active = 'true'"

GET_DOCS_FOR_UPDATE = "SELECT url_hash," \
                        "    html_hash," \
                        "    html," \
                        "    id" \
                        " FROM html_document" \
                        " WHERE last_visit_on > last_processing_data" \
                        " AND is_active = 'true'"
