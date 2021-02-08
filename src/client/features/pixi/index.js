import React, { useEffect, useContext } from "react";
import { useSelector } from "react-redux";
import { selectGlobal } from "../globalSlice";
import { ControllerContext } from "../../controllerContext";

/**
 * This is Display component
 *
 * @component
 */

const Pixi = () => {
  const controller = useContext(ControllerContext);
  const { timeData, controlRecord, posRecord } = useSelector(selectGlobal);
  const { time, controlFrame, posFrame } = timeData;

  useEffect(() => {
    // console.log(time, controlFrame);
    if (controller) {
      controller.updateDancersPos(posRecord, time, posFrame);
    }
  }, [time]);

  useEffect(() => {
    // console.log(time, controlFrame);
    if (controller) {
      controller.updateDancersControl(controlRecord, controlFrame);
    }
  }, [controlFrame]);

  useEffect(() => {
    // console.log(time, controlFrame);
    if (controller) {
      controller.updateDancersPos(posRecord, time, posFrame);
    }
  }, [posFrame]);

  // store.dispatch(setControllerPos(controller, posFrame))

  return (
    <div className="Simulator d-inline-block">
      <div id="main_stage" />
    </div>
  );
};

export default Pixi;
