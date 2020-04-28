$(document).ready(function() {
    const app = angular.module("app", []); 
    app.controller("Ctrl", function($scope) {
        $scope.computatrums = { };
        $scope.selected_computatrum = { };
        $scope.computatrumStates = [];
        $scope.interface_buttons = [];

        $scope.selectionChanged = function(new_id_selection) {
            if(!new_id_selection) {
                selected_computatrum = { };
            }
            else {
                selected_computatrum = computatrums.find(function(c) {
                    return c.id = new_id_selection;
                });
            }
        }


        $scope.setProperty = function(key, value) {
            const http = new XMLHttpRequest();
            http.open("POST", `${location.hostname}/computatrums/${$scope.selected_computatrum.id}/${key}`, true);
            http.send(value);
        }

        $(document).on("keydown", function(event) {
            switch(event.keyCode || window.event) {
                case 38: //up arrow
                    break;
                case 39: //right arrow
                    break;
                case 40: //down arrow
                    break;
                case 37: //left arrow
                    break;
                default:
            }
        });

        function setComputatrumStates() {
            const http = new XMLHttpRequest();
            http.open("GET", `${location.hostname}/api/computatrum_states`, true);
            http.onreadystatechange = function() {
                if(http.readyState == 2 && http.status == 200) {
                    $scope.computatrumStates = JSON.parse(http.responseText);
                }
            };
            http.send();
        }

        function setInterfaceButtons() {
            const http = new XMLHttpRequest();
            http.open("GET", `${location.hostname}/api/interface_buttons`, true);
            http.onreadystatechange = function() {
                if(http.readyState == 2 && http.status == 200) {
                    $scope.interface_buttons = JSON.parse(http.responseText);
                }
            };
            http.send();
        }
        
        function update() {
            //poll server for updates
            const http = new XMLHttpRequest();
            http.open("GET", `${location.hostname}/computatrums`, true);
            http.onreadystatechange(function() {
                if(http.readyState == 2 && http.status == 200) {
                    $scope.computatrums = JSON.parse(http.responseText);
                }
            });
            http.send();
        }

        setComputatrumStates()
        setInterfaceButtons()
        setTimeout(
            function() {
                update();
            }, 
            (
                $scope.selected_computatrum['ideal_fps'] ? 
                1000 / $scope.selected_computatrum['ideal_fps'] :
                100
            ) * 10
        );
    });

    //make button interface circular
    const interfaceButtons = $("$button_pad").children;
    const numButtons = interfaceButtons.length;
    for(let buttonNum = 0; buttonNum < numButtons; buttonNum++) {
        //TODO find actual names for x and y
        const radius = 70
        interfaceButtons[buttonNum].x = (radius * Math.cos(2 * Math.PI * (buttonNum / numButtons))).toString(10) + "%";
        interfaceButtons[buttonNum].y = (radius * Math.sin(2 * Math.PI * (buttonNum / numButtons))).toString(10) + "%";
    }
});