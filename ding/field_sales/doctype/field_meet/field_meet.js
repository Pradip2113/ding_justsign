// Copyright (c) 2024, manoj and contributors
// For license information, please see license.txt


frappe.ui.form.on('Field Meet', {
	setup: function(frm) {
        frm.set_query("get_from", function(doc) {
            return {
                filters: [
                    ['DocType', 'name', 'in', ['Customer', 'Lead','Suspect','Prospect']]
                ]
            };
        });
    }
});
  
frappe.ui.form.on("Field Meet", {
    onload: function(frm) {
        // Make the Data fields visible
        frm.toggle_display(['check_in_time', 'check_out_time', 'duration', 'creator'], true);

        // Set the "Creator" field to the user who submitted the document (Doc Owner)
        frm.set_value('creator', frm.doc.owner);
    },

    
    refresh: function(frm) {
        frm.add_custom_button(__('Log Location'), function() {
            // Get user's current location and save latitude and longitude to the "Logged Geo-Location" field
            navigator.geolocation.getCurrentPosition(function(position) {
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                console.log('Latitude:', latitude);
                console.log('Longitude:', longitude);

                // Set the "Logged Geo-Location" field
                frm.set_value('logged_geo_location', latitude + ',' + longitude);
            });
        });

        

        // Add POS button
        // frm.add_custom_button(__('POS'), function() {
        //     // Open POS URL with customer prefilled
        //     var customer = frm.doc.customer;
        //     if (customer) {
        //         var posUrl = `${frappe.urllib.get_base_url()}/app/point-of-sale?customer=${encodeURIComponent(customer)}`;
        //         window.open(posUrl, '_blank');
        //     } else {
        //         frappe.msgprint(__('Please select a customer.'));
        //     }
        // });


        // Add "Get Directions" button
        // frm.add_custom_button(__('Get Directions'), function() {
        //     var customerLocation = frm.doc.customer_location;
        //     if (isValidLatLong(customerLocation)) {
        //         var googleMapsUrl = 'https://www.google.com/maps?q=' + encodeURIComponent(customerLocation);
        //         window.open(googleMapsUrl, '_blank');
        //     } else {
        //         frappe.msgprint(__('Invalid Customer Location.'));
        //     }
        // });

        frm.add_custom_button(__('Start Meet'), function() {
            var currentTime = frappe.datetime.now_time();
            frm.set_value('check_in_time', currentTime);
        });

        frm.add_custom_button(__('End Meet'), function() {
            var currentTime = frappe.datetime.now_time();
            frm.set_value('check_out_time', currentTime);
            var checkInTime = frm.doc.check_in_time;
            var checkOutTime = frm.doc.check_out_time;
            function parseTime(timeStr) {
                const [hours, minutes, seconds] = timeStr.split(':').map(Number);
                const now = new Date();
                now.setHours(hours, minutes, seconds, 0);
                return now;
            }
            if (checkInTime && checkOutTime) {
                const startTime = parseTime(checkInTime);
                const endTime = parseTime(checkOutTime);
                const differenceMs = endTime - startTime;
                const totalSeconds = Math.floor(differenceMs / 1000);
                const hours = Math.floor(totalSeconds / 3600);
                const minutes = Math.floor((totalSeconds % 3600) / 60);
                const seconds = totalSeconds % 60;
                const formattedHours = String(hours).padStart(2, '0');
                const formattedMinutes = String(minutes).padStart(2, '0');
                const formattedSeconds = String(seconds).padStart(2, '0');
                var durationFormatted = `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
                frm.set_value('duration', durationFormatted);
            }
        });


        // Add "Update Customer Location" button
        // frm.add_custom_button(__('Update Customer Location'), function() {
        //     var customerLocation = frm.doc.customer_location;
        //     if (!customerLocation || !isValidLatLong(customerLocation)) {
        //         var customerName = frm.doc.customer;
        //         if (customerName) {
        //             var customerUrl = frappe.urllib.get_base_url() + '/app/customer/' + customerName;
        //             window.open(customerUrl, '_blank');
        //         } else {
        //             frappe.msgprint(__('Please select a customer.'));
        //         }
        //     }
        // });
    },

    customer_location: function(frm) {
        calculateAndSetDistance(frm);
    },

    logged_geo_location: function(frm) {
        calculateAndSetDistance(frm);
    },

    after_save: function(frm) {
        // Display the rating after the document is saved
        frm.doc.__onload.rating && frm.dashboard.set_headline_alert('Rating', frm.doc.__onload.rating, "blue");
    }
});