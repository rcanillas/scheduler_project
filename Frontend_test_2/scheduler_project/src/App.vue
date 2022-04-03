<script setup>
import { ref } from "vue";

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

function onInput(e) {
  angle.value = e.target.value;
  circle_path = describeArc(
    circle_radius,
    circle_radius,
    circle_radius - circle_radius / 3 / 2,
    0,
    angle.value
  );
  circle_quotient = angle.value / 360;
}

const circle_radius = 150;
const angle = ref("270");
let circle_path = describeArc(
  circle_radius,
  circle_radius,
  circle_radius - circle_radius / 3 / 2,
  0,
  angle.value
);
let circle_quotient = angle.value / 360;
const task_label = ref("What do I want to do ?");
const task_name = ref("");
const time_label = ref("How long do I want to do it ?");
</script>

<template>
  <p class="text">{{ task_label }}</p>
  <input v-model="task_name" placeholder="My task here" />
  <p class="text">{{ time_label }}</p>
  <div class="timer_container">
    <input class="time_input" :placeholder="circle_quotient" />
    <svg
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
  <div></div>
  <button class="button">Let's schedule it !</button>
</template>

<style>
.text {
  color: #8497ff;
}
.button {
  background: #8497ff;
  color: white;
}
.timer_container {
  position: relative;
}
.time_input {
  position: absolute;
  top: 45%;
  width: 10%;
  left: 12%;
}
</style>
