
$(document).ready(function () {
    // Declare tableData outside the click handler
    var tableData = {};

    var data_ = [];
    $('#table3 td').each(function () {
        data_.push($(this).text());
    });

    var newArray = $.map(data_, function (value) {
        return value.replace(/[\n\s]/g, '')
    });

    // Intercept the button click event
    $("#saveData").click(function () {
        tableData = {
            'table1_data': collectTableData('#table1 input'),
            'table2_data': collectTable2Data(),
            'table3_data': newArray
            // Add more tables as needed
        };

        function collectTableData(selector) {
            // Collect data from the specified input fields within a table
            var tableData = [];
            $(selector).each(function () {
                tableData.push($(this).val());
            });
            return tableData;
        }

        function collectTable2Data() {
            // Collect data from both input and textarea for table2
            var table2Data = [];
            $('#table2 tbody tr').each(function () {
                var label = $(this).find('td:eq(0)').text().trim();
                var content = $(this).find('td:eq(1) :input').val() || $(this).find('td:eq(1)').text().trim();

                var rowData = {
                    'label': label,
                    'content': content
                };

                table2Data.push(rowData);
            });
            return table2Data;
        }

        console.log("---------tableData-------------", tableData)


        // >>--------------- Converting the table1Data into the payload ---------------<<
        var table1Data = tableData.table1_data;

        // Define the keys for each column
        var keysTable1 = ["Registration_no", "Registration_date", "First_registration_date", "Makers_serial_no", "Trade_maker_vehicle", "Engine_model"];

        // Initialize an array to store the payloads for each row
        var table1Payload = [];

        // Calculate the number of rows based on the number of keys
        var numRowsTable1 = table1Data.length / keysTable1.length;

        // Loop through each row
        for (var rowIndexTable1 = 0; rowIndexTable1 < numRowsTable1; rowIndexTable1++) {
            var rowPayloadTable1 = {};

            // Loop through each key in the keysTable1 array
            for (var keyIndexTable1 = 0; keyIndexTable1 < keysTable1.length; keyIndexTable1++) {
                // Calculate the index in table1Data based on rowIndexTable1 and keyIndexTable1
                var dataIndexTable1 = rowIndexTable1 * keysTable1.length + keyIndexTable1;

                // Add the key-value pair to rowPayloadTable1
                rowPayloadTable1[keysTable1[keyIndexTable1]] = table1Data[dataIndexTable1];
            }

            // Add the transformed entry to the array
            table1Payload.push(rowPayloadTable1);
        }

        // Now 'table1Payload' contains the desired format for each row in table1_data
        // console.log("table 1=======>>", table1Payload);

        // >>--------------- Converting the table2Data into the payload ---------------<<
        var table2Data = tableData.table2_data;
        var bookingConformationPayload = {};

        console.log("tabletodata", table2Data)

        // Define the keys for each column in the desired format
        var keysTable2 = {
            'Actual Shipper': 'ActualShipper',
            'Booking Number': 'BookingNumber',
            'Vessel Number': 'Vessel_and_voyage_no',
            'B/L Original': 'B/LOriginal',
            'Port Of Loading': 'PortOfLoading',
            'Place Of Delivery': 'PlaceOfDelivery',
            'Port Of Discharge': 'PortOfDischarge',
            'Port Of Receipt': 'PortOfReceipt',
            'FREIGHT': 'Freight',
            'B/L PLACE OF ISSUE': 'B/LPlaceOfIssue',
            'SHIPPER': 'shipper',
            'CONSIGNEE': 'consignee',
            'NOTIFY': 'notify'
        };

        // Loop through each row of table2_data
        for (var i = 0; i < table2Data.length; i += 1) {
            var label = table2Data[i].label;
            var content = table2Data[i].content;

            // Find the corresponding key for the label
            var key = keysTable2[label];

            // If a matching key is found, add the content to the corresponding key in the payload
            if (key) {
                bookingConformationPayload[key] = content;
            }
        }

        // Now 'bookingConformationPayload' contains the desired format
        // console.log("Table 2: ", bookingConformationPayload);

        // >>--------------- Converting the table3Data into the payload ---------------<<
        var table3Data = tableData.table3_data;
        // Define the keys for each column
        // var keys = ["S.No.", "Year", "Maker", "Name", "Recno.", "Chassis No.",
        //     "Weight", "Length", "Width", "Height", "MEAS", 'Engine Power'];
        var keys = Array.from(document.getElementById('table3').getElementsByTagName('th'), th => th.textContent);
        // Initialize an array to store the payloads for each row
        var table3Payload = [];

        // Calculate the number of rows based on the number of keys
        var numRows = table3Data.length / keys.length;

        // Loop through each row
        for (var rowIndex = 0; rowIndex < numRows; rowIndex++) {
            var rowPayload = {};

            // Loop through each key in the keys array
            for (var keyIndex = 0; keyIndex < keys.length; keyIndex++) {
                // Calculate the index in table3Data based on rowIndex and keyIndex
                var dataIndex = rowIndex * keys.length + keyIndex;

                // Add the key-value pair to rowPayload
                rowPayload[keys[keyIndex]] = table3Data[dataIndex];
            }

            // Add the transformed entry to the array
            table3Payload.push(rowPayload);
        }


        // Now 'table3Payload' contains the desired format for each row
        // console.log("table 3=======>>", table3Payload);
        // var client = '{{ icm }}';
        // var mediator = '{{ icm1 }}';
        // var shipping_comp_name = '{{shipping_comp_name}}';
        // const payload = {

        //     "Client_Company": client,
        //     "booking_comp_name": mediator,
        //     "shipping_comp_name": shipping_comp_name,

        //     "booking_conformation":
        //         bookingConformationPayload
        //     ,
        //     "Invoice":
        //         table3Payload
        //     ,
        //     "Masho":
        //         table1Payload

        // };
        // console.log("payload", payload);

        // // Send data to the server using AJAX
        // $.ajax({
        //     type: 'POST',
        //     url: '/update_data/',
        //     data: JSON.stringify({ payload: payload }, (key, value) => (typeof value === 'string' ? value.replace(/'/g, '"') : value), 2),
        //     contentType: 'application/json; charset=utf-8',
        //     dataType: 'json',
        //     success: function (data) {
        //         console.log('Data successfully submitted:', data);
        //     },
        //     error: function (error) {
        //         console.log('Error:', error);
        //     }
        // });

    });
});