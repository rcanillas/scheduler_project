<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

onMounted(() => {
  svg_x.value = circle.value.getBoundingClientRect().left;
  svg_y.value = circle.value.getBoundingClientRect().top;
});

function postTask() {
  let task = { taskName: task_name.value, taskDuration: selected_time_in_min };
  console.log(task)
  axios.post("http://localhost:5000", task);
}

function getValueString(selected_time_in_min) {
  let value_string;
  let hour_value = Math.floor(selected_time_in_min / 60);
  let minutes_value = Math.floor(selected_time_in_min % 60);
  if (hour_value > 0) {
    value_string =
      hour_value.toString() + " h " + minutes_value.toString() + " min";
  } else {
    value_string = minutes_value.toString() + " min";
  }
  return value_string;
}

function mouseCaptureToggle() {
  console.log("Toggle value is:" + start_capture.value);
  start_capture.value = !start_capture.value;
}

function mouseCapture(e) {
  if (start_capture.value) {
    let mouse_x = e.clientX;
    let mouse_y = e.clientY;
    let d_x = mouse_x - (svg_x.value + circle_radius);
    let d_y = mouse_y - (svg_y.value + circle_radius);
    angle.value = Math.floor(
      360 - (Math.atan2(d_x, d_y) * (180 / Math.PI) + 180)
    );
    console.log("Dx:" + d_x + " Dy:" + d_y + " Angle: " + angle.value);
    update_circle(angle);
  }
}

function update_circle(angle) {
  circle_path.value = describeArc(
    circle_radius,
    circle_radius,
    circle_radius - circle_radius / 3 / 2,
    0,
    angle.value
  );
  console.log(circle_path.value);
  circle_quotient = angle.value / 360;
  selected_time_in_min = max_time_in_min * circle_quotient;
  value_string.value = getValueString(selected_time_in_min);
}

function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
  let angleInRadians = ((angleInDegrees - 90) * Math.PI) / 180.0;

  return {
    x: centerX + radius * Math.cos(angleInRadians),
    y: centerY + radius * Math.sin(angleInRadians),
  };
}

function describeArc(x, y, radius, startAngle, endAngle) {
  let start = polarToCartesian(x, y, radius, endAngle);
  let end = polarToCartesian(x, y, radius, startAngle);
  let largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  let M = ["M", Math.floor(start.x), Math.floor(start.y)].join(" ");
  let A =
    "A " +
    [
      [radius, radius].join(" "),
      "0",
      [largeArcFlag, 0].join(" "),
      [Math.floor(end.x), end.y].join(" "),
    ].join(",");
  return M + " " + A;
}

function timeFromInputString(e) {
  let timeStrings = e.target.value.split(" ");
  if (timeStrings.length === 2) {
    selected_time_in_min = parseInt(timeStrings[0]);
  } else {
    selected_time_in_min =
      parseInt(timeStrings[0]) * 60 + parseInt(timeStrings[2]);
  }
  let time_quotient = selected_time_in_min / max_time_in_min;
  angle.value = 360 * time_quotient;
  //console.log(selected_time_in_min, time_quotient, angle.value);
  update_circle(angle);
}

const circle_radius = 150;
let angle = ref(270);
let circle_path = ref(
  describeArc(
    circle_radius,
    circle_radius,
    circle_radius - circle_radius / 3 / 2,
    0,
    angle.value
  )
);

const max_time_in_min = 120;
let circle_quotient = angle.value / 360;
let selected_time_in_min = max_time_in_min * circle_quotient;
let value_string = ref(getValueString(selected_time_in_min));
let start_capture = ref(false);
let svg_x = ref(0);
let svg_y = ref(0);
let circle = ref(null);
const task_label = ref("What do I want to do ?");
const task_name = ref("");
const time_label = ref("How long do I want to do it ?");
</script>

<template>
  <div class="center_div">
    <p class="text">{{ task_label }}</p>
    <input v-model="task_name" placeholder="My task here" />
    <p class="text">{{ time_label }}</p>
  </div>
  <div
    class="center_div"
    @mouseup="mouseCaptureToggle"
    @mousedown="mouseCaptureToggle"
    @mousemove="mouseCapture"
  >
    <svg
      ref="circle"
      class="circle_component"
      :width="circle_radius * 2"
      :height="circle_radius * 2"
    >
      <circle
        :cx="circle_radius"
        :cy="circle_radius"
        :r="circle_radius"
        fill="lightgrey"
      />
      <circle
        :cx="circle_radius"
        :cy="circle_radius"
        :r="circle_radius - circle_radius / 3"
        fill="white"
      />
      <path
        :d="circle_path"
        stroke="#8497FF"
        fill="None"
        :stroke-width="circle_radius / 3"
        stroke-linecap="round"
      />
    </svg>
  </div>
  <div class="center_div">
    <input
      :width="circle_radius"
      class="circle_text"
      :value="value_string"
      @change="timeFromInputString"
    />
  </div>

  <div class="center_div">
    <button @click="postTask" class="button">Let's schedule it !</button>
  </div>
</template>

<style>
.circle_component {
}
.circle_text {
  width: 100px;
  transform: translate(0%, -165px);
  border: 0;
  text-align: center;
}
.text {
  color: #8497ff;
  text-align: center;
}
.button {
  background: #8497ff;
  color: white;
}

.center_div {
  text-align: center;
}
</style>
