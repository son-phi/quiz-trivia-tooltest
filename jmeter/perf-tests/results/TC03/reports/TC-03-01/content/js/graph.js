/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 6154.0, "minX": 0.0, "maxY": 29744.0, "series": [{"data": [[0.0, 6154.0], [0.1, 6154.0], [0.2, 6154.0], [0.3, 6154.0], [0.4, 6154.0], [0.5, 6154.0], [0.6, 6154.0], [0.7, 6154.0], [0.8, 6154.0], [0.9, 6154.0], [1.0, 6154.0], [1.1, 6154.0], [1.2, 6154.0], [1.3, 6154.0], [1.4, 6154.0], [1.5, 6154.0], [1.6, 6154.0], [1.7, 6154.0], [1.8, 6154.0], [1.9, 6154.0], [2.0, 6154.0], [2.1, 6154.0], [2.2, 6154.0], [2.3, 6154.0], [2.4, 6154.0], [2.5, 6154.0], [2.6, 6154.0], [2.7, 6154.0], [2.8, 6154.0], [2.9, 6154.0], [3.0, 6154.0], [3.1, 6154.0], [3.2, 6154.0], [3.3, 6154.0], [3.4, 6154.0], [3.5, 6154.0], [3.6, 6154.0], [3.7, 6154.0], [3.8, 6154.0], [3.9, 6154.0], [4.0, 6154.0], [4.1, 6154.0], [4.2, 6154.0], [4.3, 6154.0], [4.4, 6154.0], [4.5, 6154.0], [4.6, 6154.0], [4.7, 6154.0], [4.8, 6154.0], [4.9, 6154.0], [5.0, 6154.0], [5.1, 6154.0], [5.2, 6154.0], [5.3, 6154.0], [5.4, 6154.0], [5.5, 6154.0], [5.6, 6154.0], [5.7, 6154.0], [5.8, 6154.0], [5.9, 6154.0], [6.0, 6154.0], [6.1, 6154.0], [6.2, 6154.0], [6.3, 6154.0], [6.4, 6154.0], [6.5, 6154.0], [6.6, 6154.0], [6.7, 8461.0], [6.8, 8461.0], [6.9, 8461.0], [7.0, 8461.0], [7.1, 8461.0], [7.2, 8461.0], [7.3, 8461.0], [7.4, 8461.0], [7.5, 8461.0], [7.6, 8461.0], [7.7, 8461.0], [7.8, 8461.0], [7.9, 8461.0], [8.0, 8461.0], [8.1, 8461.0], [8.2, 8461.0], [8.3, 8461.0], [8.4, 8461.0], [8.5, 8461.0], [8.6, 8461.0], [8.7, 8461.0], [8.8, 8461.0], [8.9, 8461.0], [9.0, 8461.0], [9.1, 8461.0], [9.2, 8461.0], [9.3, 8461.0], [9.4, 8461.0], [9.5, 8461.0], [9.6, 8461.0], [9.7, 8461.0], [9.8, 8461.0], [9.9, 8461.0], [10.0, 8461.0], [10.1, 8461.0], [10.2, 8461.0], [10.3, 8461.0], [10.4, 8461.0], [10.5, 8461.0], [10.6, 8461.0], [10.7, 8461.0], [10.8, 8461.0], [10.9, 8461.0], [11.0, 8461.0], [11.1, 8461.0], [11.2, 8461.0], [11.3, 8461.0], [11.4, 8461.0], [11.5, 8461.0], [11.6, 8461.0], [11.7, 8461.0], [11.8, 8461.0], [11.9, 8461.0], [12.0, 8461.0], [12.1, 8461.0], [12.2, 8461.0], [12.3, 8461.0], [12.4, 8461.0], [12.5, 8461.0], [12.6, 8461.0], [12.7, 8461.0], [12.8, 8461.0], [12.9, 8461.0], [13.0, 8461.0], [13.1, 8461.0], [13.2, 8461.0], [13.3, 8461.0], [13.4, 10012.0], [13.5, 10012.0], [13.6, 10012.0], [13.7, 10012.0], [13.8, 10012.0], [13.9, 10012.0], [14.0, 10012.0], [14.1, 10012.0], [14.2, 10012.0], [14.3, 10012.0], [14.4, 10012.0], [14.5, 10012.0], [14.6, 10012.0], [14.7, 10012.0], [14.8, 10012.0], [14.9, 10012.0], [15.0, 10012.0], [15.1, 10012.0], [15.2, 10012.0], [15.3, 10012.0], [15.4, 10012.0], [15.5, 10012.0], [15.6, 10012.0], [15.7, 10012.0], [15.8, 10012.0], [15.9, 10012.0], [16.0, 10012.0], [16.1, 10012.0], [16.2, 10012.0], [16.3, 10012.0], [16.4, 10012.0], [16.5, 10012.0], [16.6, 10012.0], [16.7, 10012.0], [16.8, 10012.0], [16.9, 10012.0], [17.0, 10012.0], [17.1, 10012.0], [17.2, 10012.0], [17.3, 10012.0], [17.4, 10012.0], [17.5, 10012.0], [17.6, 10012.0], [17.7, 10012.0], [17.8, 10012.0], [17.9, 10012.0], [18.0, 10012.0], [18.1, 10012.0], [18.2, 10012.0], [18.3, 10012.0], [18.4, 10012.0], [18.5, 10012.0], [18.6, 10012.0], [18.7, 10012.0], [18.8, 10012.0], [18.9, 10012.0], [19.0, 10012.0], [19.1, 10012.0], [19.2, 10012.0], [19.3, 10012.0], [19.4, 10012.0], [19.5, 10012.0], [19.6, 10012.0], [19.7, 10012.0], [19.8, 10012.0], [19.9, 10012.0], [20.0, 10627.0], [20.1, 10627.0], [20.2, 10627.0], [20.3, 10627.0], [20.4, 10627.0], [20.5, 10627.0], [20.6, 10627.0], [20.7, 10627.0], [20.8, 10627.0], [20.9, 10627.0], [21.0, 10627.0], [21.1, 10627.0], [21.2, 10627.0], [21.3, 10627.0], [21.4, 10627.0], [21.5, 10627.0], [21.6, 10627.0], [21.7, 10627.0], [21.8, 10627.0], [21.9, 10627.0], [22.0, 10627.0], [22.1, 10627.0], [22.2, 10627.0], [22.3, 10627.0], [22.4, 10627.0], [22.5, 10627.0], [22.6, 10627.0], [22.7, 10627.0], [22.8, 10627.0], [22.9, 10627.0], [23.0, 10627.0], [23.1, 10627.0], [23.2, 10627.0], [23.3, 10627.0], [23.4, 10627.0], [23.5, 10627.0], [23.6, 10627.0], [23.7, 10627.0], [23.8, 10627.0], [23.9, 10627.0], [24.0, 10627.0], [24.1, 10627.0], [24.2, 10627.0], [24.3, 10627.0], [24.4, 10627.0], [24.5, 10627.0], [24.6, 10627.0], [24.7, 10627.0], [24.8, 10627.0], [24.9, 10627.0], [25.0, 10627.0], [25.1, 10627.0], [25.2, 10627.0], [25.3, 10627.0], [25.4, 10627.0], [25.5, 10627.0], [25.6, 10627.0], [25.7, 10627.0], [25.8, 10627.0], [25.9, 10627.0], [26.0, 10627.0], [26.1, 10627.0], [26.2, 10627.0], [26.3, 10627.0], [26.4, 10627.0], [26.5, 10627.0], [26.6, 10627.0], [26.7, 11783.0], [26.8, 11783.0], [26.9, 11783.0], [27.0, 11783.0], [27.1, 11783.0], [27.2, 11783.0], [27.3, 11783.0], [27.4, 11783.0], [27.5, 11783.0], [27.6, 11783.0], [27.7, 11783.0], [27.8, 11783.0], [27.9, 11783.0], [28.0, 11783.0], [28.1, 11783.0], [28.2, 11783.0], [28.3, 11783.0], [28.4, 11783.0], [28.5, 11783.0], [28.6, 11783.0], [28.7, 11783.0], [28.8, 11783.0], [28.9, 11783.0], [29.0, 11783.0], [29.1, 11783.0], [29.2, 11783.0], [29.3, 11783.0], [29.4, 11783.0], [29.5, 11783.0], [29.6, 11783.0], [29.7, 11783.0], [29.8, 11783.0], [29.9, 11783.0], [30.0, 11783.0], [30.1, 11783.0], [30.2, 11783.0], [30.3, 11783.0], [30.4, 11783.0], [30.5, 11783.0], [30.6, 11783.0], [30.7, 11783.0], [30.8, 11783.0], [30.9, 11783.0], [31.0, 11783.0], [31.1, 11783.0], [31.2, 11783.0], [31.3, 11783.0], [31.4, 11783.0], [31.5, 11783.0], [31.6, 11783.0], [31.7, 11783.0], [31.8, 11783.0], [31.9, 11783.0], [32.0, 11783.0], [32.1, 11783.0], [32.2, 11783.0], [32.3, 11783.0], [32.4, 11783.0], [32.5, 11783.0], [32.6, 11783.0], [32.7, 11783.0], [32.8, 11783.0], [32.9, 11783.0], [33.0, 11783.0], [33.1, 11783.0], [33.2, 11783.0], [33.3, 11783.0], [33.4, 13576.0], [33.5, 13576.0], [33.6, 13576.0], [33.7, 13576.0], [33.8, 13576.0], [33.9, 13576.0], [34.0, 13576.0], [34.1, 13576.0], [34.2, 13576.0], [34.3, 13576.0], [34.4, 13576.0], [34.5, 13576.0], [34.6, 13576.0], [34.7, 13576.0], [34.8, 13576.0], [34.9, 13576.0], [35.0, 13576.0], [35.1, 13576.0], [35.2, 13576.0], [35.3, 13576.0], [35.4, 13576.0], [35.5, 13576.0], [35.6, 13576.0], [35.7, 13576.0], [35.8, 13576.0], [35.9, 13576.0], [36.0, 13576.0], [36.1, 13576.0], [36.2, 13576.0], [36.3, 13576.0], [36.4, 13576.0], [36.5, 13576.0], [36.6, 13576.0], [36.7, 13576.0], [36.8, 13576.0], [36.9, 13576.0], [37.0, 13576.0], [37.1, 13576.0], [37.2, 13576.0], [37.3, 13576.0], [37.4, 13576.0], [37.5, 13576.0], [37.6, 13576.0], [37.7, 13576.0], [37.8, 13576.0], [37.9, 13576.0], [38.0, 13576.0], [38.1, 13576.0], [38.2, 13576.0], [38.3, 13576.0], [38.4, 13576.0], [38.5, 13576.0], [38.6, 13576.0], [38.7, 13576.0], [38.8, 13576.0], [38.9, 13576.0], [39.0, 13576.0], [39.1, 13576.0], [39.2, 13576.0], [39.3, 13576.0], [39.4, 13576.0], [39.5, 13576.0], [39.6, 13576.0], [39.7, 13576.0], [39.8, 13576.0], [39.9, 13576.0], [40.0, 13588.0], [40.1, 13588.0], [40.2, 13588.0], [40.3, 13588.0], [40.4, 13588.0], [40.5, 13588.0], [40.6, 13588.0], [40.7, 13588.0], [40.8, 13588.0], [40.9, 13588.0], [41.0, 13588.0], [41.1, 13588.0], [41.2, 13588.0], [41.3, 13588.0], [41.4, 13588.0], [41.5, 13588.0], [41.6, 13588.0], [41.7, 13588.0], [41.8, 13588.0], [41.9, 13588.0], [42.0, 13588.0], [42.1, 13588.0], [42.2, 13588.0], [42.3, 13588.0], [42.4, 13588.0], [42.5, 13588.0], [42.6, 13588.0], [42.7, 13588.0], [42.8, 13588.0], [42.9, 13588.0], [43.0, 13588.0], [43.1, 13588.0], [43.2, 13588.0], [43.3, 13588.0], [43.4, 13588.0], [43.5, 13588.0], [43.6, 13588.0], [43.7, 13588.0], [43.8, 13588.0], [43.9, 13588.0], [44.0, 13588.0], [44.1, 13588.0], [44.2, 13588.0], [44.3, 13588.0], [44.4, 13588.0], [44.5, 13588.0], [44.6, 13588.0], [44.7, 13588.0], [44.8, 13588.0], [44.9, 13588.0], [45.0, 13588.0], [45.1, 13588.0], [45.2, 13588.0], [45.3, 13588.0], [45.4, 13588.0], [45.5, 13588.0], [45.6, 13588.0], [45.7, 13588.0], [45.8, 13588.0], [45.9, 13588.0], [46.0, 13588.0], [46.1, 13588.0], [46.2, 13588.0], [46.3, 13588.0], [46.4, 13588.0], [46.5, 13588.0], [46.6, 13588.0], [46.7, 14040.0], [46.8, 14040.0], [46.9, 14040.0], [47.0, 14040.0], [47.1, 14040.0], [47.2, 14040.0], [47.3, 14040.0], [47.4, 14040.0], [47.5, 14040.0], [47.6, 14040.0], [47.7, 14040.0], [47.8, 14040.0], [47.9, 14040.0], [48.0, 14040.0], [48.1, 14040.0], [48.2, 14040.0], [48.3, 14040.0], [48.4, 14040.0], [48.5, 14040.0], [48.6, 14040.0], [48.7, 14040.0], [48.8, 14040.0], [48.9, 14040.0], [49.0, 14040.0], [49.1, 14040.0], [49.2, 14040.0], [49.3, 14040.0], [49.4, 14040.0], [49.5, 14040.0], [49.6, 14040.0], [49.7, 14040.0], [49.8, 14040.0], [49.9, 14040.0], [50.0, 14040.0], [50.1, 14040.0], [50.2, 14040.0], [50.3, 14040.0], [50.4, 14040.0], [50.5, 14040.0], [50.6, 14040.0], [50.7, 14040.0], [50.8, 14040.0], [50.9, 14040.0], [51.0, 14040.0], [51.1, 14040.0], [51.2, 14040.0], [51.3, 14040.0], [51.4, 14040.0], [51.5, 14040.0], [51.6, 14040.0], [51.7, 14040.0], [51.8, 14040.0], [51.9, 14040.0], [52.0, 14040.0], [52.1, 14040.0], [52.2, 14040.0], [52.3, 14040.0], [52.4, 14040.0], [52.5, 14040.0], [52.6, 14040.0], [52.7, 14040.0], [52.8, 14040.0], [52.9, 14040.0], [53.0, 14040.0], [53.1, 14040.0], [53.2, 14040.0], [53.3, 14040.0], [53.4, 15539.0], [53.5, 15539.0], [53.6, 15539.0], [53.7, 15539.0], [53.8, 15539.0], [53.9, 15539.0], [54.0, 15539.0], [54.1, 15539.0], [54.2, 15539.0], [54.3, 15539.0], [54.4, 15539.0], [54.5, 15539.0], [54.6, 15539.0], [54.7, 15539.0], [54.8, 15539.0], [54.9, 15539.0], [55.0, 15539.0], [55.1, 15539.0], [55.2, 15539.0], [55.3, 15539.0], [55.4, 15539.0], [55.5, 15539.0], [55.6, 15539.0], [55.7, 15539.0], [55.8, 15539.0], [55.9, 15539.0], [56.0, 15539.0], [56.1, 15539.0], [56.2, 15539.0], [56.3, 15539.0], [56.4, 15539.0], [56.5, 15539.0], [56.6, 15539.0], [56.7, 15539.0], [56.8, 15539.0], [56.9, 15539.0], [57.0, 15539.0], [57.1, 15539.0], [57.2, 15539.0], [57.3, 15539.0], [57.4, 15539.0], [57.5, 15539.0], [57.6, 15539.0], [57.7, 15539.0], [57.8, 15539.0], [57.9, 15539.0], [58.0, 15539.0], [58.1, 15539.0], [58.2, 15539.0], [58.3, 15539.0], [58.4, 15539.0], [58.5, 15539.0], [58.6, 15539.0], [58.7, 15539.0], [58.8, 15539.0], [58.9, 15539.0], [59.0, 15539.0], [59.1, 15539.0], [59.2, 15539.0], [59.3, 15539.0], [59.4, 15539.0], [59.5, 15539.0], [59.6, 15539.0], [59.7, 15539.0], [59.8, 15539.0], [59.9, 15539.0], [60.0, 20592.0], [60.1, 20592.0], [60.2, 20592.0], [60.3, 20592.0], [60.4, 20592.0], [60.5, 20592.0], [60.6, 20592.0], [60.7, 20592.0], [60.8, 20592.0], [60.9, 20592.0], [61.0, 20592.0], [61.1, 20592.0], [61.2, 20592.0], [61.3, 20592.0], [61.4, 20592.0], [61.5, 20592.0], [61.6, 20592.0], [61.7, 20592.0], [61.8, 20592.0], [61.9, 20592.0], [62.0, 20592.0], [62.1, 20592.0], [62.2, 20592.0], [62.3, 20592.0], [62.4, 20592.0], [62.5, 20592.0], [62.6, 20592.0], [62.7, 20592.0], [62.8, 20592.0], [62.9, 20592.0], [63.0, 20592.0], [63.1, 20592.0], [63.2, 20592.0], [63.3, 20592.0], [63.4, 20592.0], [63.5, 20592.0], [63.6, 20592.0], [63.7, 20592.0], [63.8, 20592.0], [63.9, 20592.0], [64.0, 20592.0], [64.1, 20592.0], [64.2, 20592.0], [64.3, 20592.0], [64.4, 20592.0], [64.5, 20592.0], [64.6, 20592.0], [64.7, 20592.0], [64.8, 20592.0], [64.9, 20592.0], [65.0, 20592.0], [65.1, 20592.0], [65.2, 20592.0], [65.3, 20592.0], [65.4, 20592.0], [65.5, 20592.0], [65.6, 20592.0], [65.7, 20592.0], [65.8, 20592.0], [65.9, 20592.0], [66.0, 20592.0], [66.1, 20592.0], [66.2, 20592.0], [66.3, 20592.0], [66.4, 20592.0], [66.5, 20592.0], [66.6, 20592.0], [66.7, 20864.0], [66.8, 20864.0], [66.9, 20864.0], [67.0, 20864.0], [67.1, 20864.0], [67.2, 20864.0], [67.3, 20864.0], [67.4, 20864.0], [67.5, 20864.0], [67.6, 20864.0], [67.7, 20864.0], [67.8, 20864.0], [67.9, 20864.0], [68.0, 20864.0], [68.1, 20864.0], [68.2, 20864.0], [68.3, 20864.0], [68.4, 20864.0], [68.5, 20864.0], [68.6, 20864.0], [68.7, 20864.0], [68.8, 20864.0], [68.9, 20864.0], [69.0, 20864.0], [69.1, 20864.0], [69.2, 20864.0], [69.3, 20864.0], [69.4, 20864.0], [69.5, 20864.0], [69.6, 20864.0], [69.7, 20864.0], [69.8, 20864.0], [69.9, 20864.0], [70.0, 20864.0], [70.1, 20864.0], [70.2, 20864.0], [70.3, 20864.0], [70.4, 20864.0], [70.5, 20864.0], [70.6, 20864.0], [70.7, 20864.0], [70.8, 20864.0], [70.9, 20864.0], [71.0, 20864.0], [71.1, 20864.0], [71.2, 20864.0], [71.3, 20864.0], [71.4, 20864.0], [71.5, 20864.0], [71.6, 20864.0], [71.7, 20864.0], [71.8, 20864.0], [71.9, 20864.0], [72.0, 20864.0], [72.1, 20864.0], [72.2, 20864.0], [72.3, 20864.0], [72.4, 20864.0], [72.5, 20864.0], [72.6, 20864.0], [72.7, 20864.0], [72.8, 20864.0], [72.9, 20864.0], [73.0, 20864.0], [73.1, 20864.0], [73.2, 20864.0], [73.3, 20864.0], [73.4, 25125.0], [73.5, 25125.0], [73.6, 25125.0], [73.7, 25125.0], [73.8, 25125.0], [73.9, 25125.0], [74.0, 25125.0], [74.1, 25125.0], [74.2, 25125.0], [74.3, 25125.0], [74.4, 25125.0], [74.5, 25125.0], [74.6, 25125.0], [74.7, 25125.0], [74.8, 25125.0], [74.9, 25125.0], [75.0, 25125.0], [75.1, 25125.0], [75.2, 25125.0], [75.3, 25125.0], [75.4, 25125.0], [75.5, 25125.0], [75.6, 25125.0], [75.7, 25125.0], [75.8, 25125.0], [75.9, 25125.0], [76.0, 25125.0], [76.1, 25125.0], [76.2, 25125.0], [76.3, 25125.0], [76.4, 25125.0], [76.5, 25125.0], [76.6, 25125.0], [76.7, 25125.0], [76.8, 25125.0], [76.9, 25125.0], [77.0, 25125.0], [77.1, 25125.0], [77.2, 25125.0], [77.3, 25125.0], [77.4, 25125.0], [77.5, 25125.0], [77.6, 25125.0], [77.7, 25125.0], [77.8, 25125.0], [77.9, 25125.0], [78.0, 25125.0], [78.1, 25125.0], [78.2, 25125.0], [78.3, 25125.0], [78.4, 25125.0], [78.5, 25125.0], [78.6, 25125.0], [78.7, 25125.0], [78.8, 25125.0], [78.9, 25125.0], [79.0, 25125.0], [79.1, 25125.0], [79.2, 25125.0], [79.3, 25125.0], [79.4, 25125.0], [79.5, 25125.0], [79.6, 25125.0], [79.7, 25125.0], [79.8, 25125.0], [79.9, 25125.0], [80.0, 27012.0], [80.1, 27012.0], [80.2, 27012.0], [80.3, 27012.0], [80.4, 27012.0], [80.5, 27012.0], [80.6, 27012.0], [80.7, 27012.0], [80.8, 27012.0], [80.9, 27012.0], [81.0, 27012.0], [81.1, 27012.0], [81.2, 27012.0], [81.3, 27012.0], [81.4, 27012.0], [81.5, 27012.0], [81.6, 27012.0], [81.7, 27012.0], [81.8, 27012.0], [81.9, 27012.0], [82.0, 27012.0], [82.1, 27012.0], [82.2, 27012.0], [82.3, 27012.0], [82.4, 27012.0], [82.5, 27012.0], [82.6, 27012.0], [82.7, 27012.0], [82.8, 27012.0], [82.9, 27012.0], [83.0, 27012.0], [83.1, 27012.0], [83.2, 27012.0], [83.3, 27012.0], [83.4, 27012.0], [83.5, 27012.0], [83.6, 27012.0], [83.7, 27012.0], [83.8, 27012.0], [83.9, 27012.0], [84.0, 27012.0], [84.1, 27012.0], [84.2, 27012.0], [84.3, 27012.0], [84.4, 27012.0], [84.5, 27012.0], [84.6, 27012.0], [84.7, 27012.0], [84.8, 27012.0], [84.9, 27012.0], [85.0, 27012.0], [85.1, 27012.0], [85.2, 27012.0], [85.3, 27012.0], [85.4, 27012.0], [85.5, 27012.0], [85.6, 27012.0], [85.7, 27012.0], [85.8, 27012.0], [85.9, 27012.0], [86.0, 27012.0], [86.1, 27012.0], [86.2, 27012.0], [86.3, 27012.0], [86.4, 27012.0], [86.5, 27012.0], [86.6, 27012.0], [86.7, 28307.0], [86.8, 28307.0], [86.9, 28307.0], [87.0, 28307.0], [87.1, 28307.0], [87.2, 28307.0], [87.3, 28307.0], [87.4, 28307.0], [87.5, 28307.0], [87.6, 28307.0], [87.7, 28307.0], [87.8, 28307.0], [87.9, 28307.0], [88.0, 28307.0], [88.1, 28307.0], [88.2, 28307.0], [88.3, 28307.0], [88.4, 28307.0], [88.5, 28307.0], [88.6, 28307.0], [88.7, 28307.0], [88.8, 28307.0], [88.9, 28307.0], [89.0, 28307.0], [89.1, 28307.0], [89.2, 28307.0], [89.3, 28307.0], [89.4, 28307.0], [89.5, 28307.0], [89.6, 28307.0], [89.7, 28307.0], [89.8, 28307.0], [89.9, 28307.0], [90.0, 28307.0], [90.1, 28307.0], [90.2, 28307.0], [90.3, 28307.0], [90.4, 28307.0], [90.5, 28307.0], [90.6, 28307.0], [90.7, 28307.0], [90.8, 28307.0], [90.9, 28307.0], [91.0, 28307.0], [91.1, 28307.0], [91.2, 28307.0], [91.3, 28307.0], [91.4, 28307.0], [91.5, 28307.0], [91.6, 28307.0], [91.7, 28307.0], [91.8, 28307.0], [91.9, 28307.0], [92.0, 28307.0], [92.1, 28307.0], [92.2, 28307.0], [92.3, 28307.0], [92.4, 28307.0], [92.5, 28307.0], [92.6, 28307.0], [92.7, 28307.0], [92.8, 28307.0], [92.9, 28307.0], [93.0, 28307.0], [93.1, 28307.0], [93.2, 28307.0], [93.3, 28307.0], [93.4, 29744.0], [93.5, 29744.0], [93.6, 29744.0], [93.7, 29744.0], [93.8, 29744.0], [93.9, 29744.0], [94.0, 29744.0], [94.1, 29744.0], [94.2, 29744.0], [94.3, 29744.0], [94.4, 29744.0], [94.5, 29744.0], [94.6, 29744.0], [94.7, 29744.0], [94.8, 29744.0], [94.9, 29744.0], [95.0, 29744.0], [95.1, 29744.0], [95.2, 29744.0], [95.3, 29744.0], [95.4, 29744.0], [95.5, 29744.0], [95.6, 29744.0], [95.7, 29744.0], [95.8, 29744.0], [95.9, 29744.0], [96.0, 29744.0], [96.1, 29744.0], [96.2, 29744.0], [96.3, 29744.0], [96.4, 29744.0], [96.5, 29744.0], [96.6, 29744.0], [96.7, 29744.0], [96.8, 29744.0], [96.9, 29744.0], [97.0, 29744.0], [97.1, 29744.0], [97.2, 29744.0], [97.3, 29744.0], [97.4, 29744.0], [97.5, 29744.0], [97.6, 29744.0], [97.7, 29744.0], [97.8, 29744.0], [97.9, 29744.0], [98.0, 29744.0], [98.1, 29744.0], [98.2, 29744.0], [98.3, 29744.0], [98.4, 29744.0], [98.5, 29744.0], [98.6, 29744.0], [98.7, 29744.0], [98.8, 29744.0], [98.9, 29744.0], [99.0, 29744.0], [99.1, 29744.0], [99.2, 29744.0], [99.3, 29744.0], [99.4, 29744.0], [99.5, 29744.0], [99.6, 29744.0], [99.7, 29744.0], [99.8, 29744.0], [99.9, 29744.0], [100.0, 29744.0]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 6100.0, "maxY": 2.0, "series": [{"data": [[8400.0, 1.0], [10000.0, 1.0], [10600.0, 1.0], [11700.0, 1.0], [13500.0, 2.0], [14000.0, 1.0], [15500.0, 1.0], [20500.0, 1.0], [20800.0, 1.0], [6100.0, 1.0], [25100.0, 1.0], [27000.0, 1.0], [28300.0, 1.0], [29700.0, 1.0]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 29700.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 2.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 14.0, "series": [{"data": [], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [[2.0, 14.0]], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [[3.0, 1.0]], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 3.0, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 2.2, "minX": 1.77660504E12, "maxY": 4.699999999999999, "series": [{"data": [[1.7766051E12, 2.2], [1.77660504E12, 4.699999999999999]], "isOverall": false, "label": "TC-03 Chatbot RAG Flow", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7766051E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 9401.0, "minX": 1.0, "maxY": 21173.5, "series": [{"data": [[4.0, 9401.0], [2.0, 18512.0], [1.0, 10627.0], [5.0, 19603.285714285714], [3.0, 21173.5]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}, {"data": [[3.866666666666666, 17028.266666666666]], "isOverall": false, "label": "TC03-01 Ask RAG-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 5.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 108.16666666666667, "minX": 1.77660504E12, "maxY": 784.4666666666667, "series": [{"data": [[1.7766051E12, 448.2], [1.77660504E12, 784.4666666666667]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.7766051E12, 108.16666666666667], [1.77660504E12, 216.63333333333333]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7766051E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 16542.600000000002, "minX": 1.77660504E12, "maxY": 17999.6, "series": [{"data": [[1.7766051E12, 17999.6], [1.77660504E12, 16542.600000000002]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7766051E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 16540.600000000002, "minX": 1.77660504E12, "maxY": 17997.0, "series": [{"data": [[1.7766051E12, 17997.0], [1.77660504E12, 16540.600000000002]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7766051E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 23.2, "minX": 1.77660504E12, "maxY": 101.9, "series": [{"data": [[1.7766051E12, 23.2], [1.77660504E12, 101.9]], "isOverall": false, "label": "TC03-01 Ask RAG", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7766051E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 8461.0, "minX": 1.77660504E12, "maxY": 29744.0, "series": [{"data": [[1.7766051E12, 28307.0], [1.77660504E12, 29744.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.7766051E12, 10012.0], [1.77660504E12, 8461.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.7766051E12, 28307.0], [1.77660504E12, 29744.0]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.7766051E12, 28307.0], [1.77660504E12, 29744.0]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.7766051E12, 14040.0], [1.77660504E12, 15539.0]], "isOverall": false, "label": "Median", "isController": false}, {"data": [[1.7766051E12, 28307.0], [1.77660504E12, 29744.0]], "isOverall": false, "label": "95th percentile", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7766051E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 6154.0, "minX": 1.0, "maxY": 18065.5, "series": [{"data": [[2.0, 11800.0], [1.0, 18065.5]], "isOverall": false, "label": "Successes", "isController": false}, {"data": [[1.0, 6154.0]], "isOverall": false, "label": "Failures", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 2.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 6154.0, "minX": 1.0, "maxY": 18064.5, "series": [{"data": [[2.0, 11797.5], [1.0, 18064.5]], "isOverall": false, "label": "Successes", "isController": false}, {"data": [[1.0, 6154.0]], "isOverall": false, "label": "Failures", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 2.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.77660498E12, "maxY": 0.2, "series": [{"data": [[1.77660498E12, 0.016666666666666666], [1.7766051E12, 0.03333333333333333], [1.77660504E12, 0.2]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7766051E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.77660504E12, "maxY": 0.15, "series": [{"data": [[1.7766051E12, 0.08333333333333333], [1.77660504E12, 0.15]], "isOverall": false, "label": "200", "isController": false}, {"data": [[1.77660504E12, 0.016666666666666666]], "isOverall": false, "label": "500", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.7766051E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.77660504E12, "maxY": 0.15, "series": [{"data": [[1.7766051E12, 0.08333333333333333], [1.77660504E12, 0.15]], "isOverall": false, "label": "TC03-01 Ask RAG-success", "isController": false}, {"data": [[1.77660504E12, 0.016666666666666666]], "isOverall": false, "label": "TC03-01 Ask RAG-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7766051E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 0.016666666666666666, "minX": 1.77660504E12, "maxY": 0.15, "series": [{"data": [[1.7766051E12, 0.08333333333333333], [1.77660504E12, 0.15]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [[1.77660504E12, 0.016666666666666666]], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.7766051E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 25200000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

