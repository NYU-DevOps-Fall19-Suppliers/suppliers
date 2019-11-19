$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        res = JSON.parse(res);
        $("#supplier_id").val(res._id.$oid);
        $("#supplierName").val(res.supplierName);
        $("#address").val(res.address);
        $("#productIdList").val(res.productIdList);
        $("#averageRating").val(res.averageRating);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#supplierName").val("");
        $("#address").val("");
        $("#productIdList").val("");
        $("#averageRating").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Supplier
    // ****************************************

    $("#create-btn").click(function () {

        var supplierName = $("#supplierName").val();
        var address = $("#address").val();
        var productIdList = $("#productIdList").val().replace(" ", "").split(",");
        var averageRating = $("#averageRating").val();

        var data = {
            "supplierName": supplierName,
            "address": address,
            "productIdList": productIdList,
            "averageRating": averageRating
        };

        console.log(JSON.stringify(data));

        var ajax = $.ajax({
            type: "POST",
            url: "/suppliers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Supplier
    // ****************************************

    $("#update-btn").click(function () {

        var supplier_id = $("#supplier_id").val();
        var supplierName = $("#supplierName").val();
        var address = $("#address").val();
        var productIdList = $("#productIdList").val().replace(" ", "").split(",");
        var averageRating = $("#averageRating").val();

        var data = {
            "supplierName": supplierName,
            "address": address,
            "productIdList": productIdList,
            "averageRating": averageRating
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/suppliers/" + supplier_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Supplier
    // ****************************************

    $("#retrieve-btn").click(function () {

        var supplier_id = $("#supplier_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/suppliers/" + supplier_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            console.log("Retrieve data is");
            console.log(res);
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Supplier
    // ****************************************

    $("#delete-btn").click(function () {

        var supplier_id = $("#supplier_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/suppliers/" + supplier_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Supplier has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#supplier_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Supplier
    // ****************************************

    $("#search-btn").click(function () {

        var supplierName = $("#supplierName").val();
        var address = $("#address").val();
        var productIdList = $("#productIdList").val().replace(" ", "").split(",");
        var averageRating = $("#averageRating").val();

        var queryString = ""

        if (supplierName) {
            queryString += 'supplierName=' + supplierName
        }
        // if (address) {
        //     if (queryString.length > 0) {
        //         queryString += '&address=' + address
        //     } else {
        //         queryString += 'address=' + address
        //     }
        // }
        // if (averageRating) {
        //     if (queryString.length > 0) {
        //         queryString += '&averageRating=' + averageRating
        //     } else {
        //         queryString += 'averageRating=' + averageRating
        //     }
        // }
        // if (averageRating) {
        //     queryString += 'averageRating=' + averageRating.toString()
        // }


        var ajax = $.ajax({
            type: "GET",
            url: "/suppliers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">supplier_id</th>'
            header += '<th style="width:40%">supplierName</th>'
            header += '<th style="width:40%">address</th>'
            header += '<th style="width:10%">productIdList</th>'
            header += '<th style="width:40%">averageRating</th></tr>'
            $("#search_results").append(header);
            var firstSupplier = "";
            res = JSON.parse(res)
            for(var i = 0; i < res.length; i++) {
                console.log(res[i]);
                var supplier = res[i];
                var row = "<tr><td>"+supplier._id.$oid+"</td><td>"+supplier.supplierName+"</td><td>"+supplier.address+"</td><td>"+supplier.productIdList+"</td><td>"+supplier.averageRating+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstSupplier = supplier;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstSupplier != "") {
                update_form_data(firstSupplier)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
