"use client";

import VideoRecorder from "@/components/mock-interview/VideoRecorder";
import QuestionsPanel from "@/components/mock-interview/QuestionsPanel";
import { useState } from "react";
import questions from "@/data/questions.json";
import Timer from "@/components/common/Timer";
import Tabs from "@/components/common/Tabs";
import Question from "@/components/mock-interview/Question";
import PreviousAttemptSummary from "@/components/mock-interview/PreviousAttempSummary";
import AttemptHistory from "@/components/mock-interview/AttemptHistory";

const tabs = ["Question", "Previous Attempts"];
const attempts = [
  {
    id: 1,
    date: new Date(),
  },
  {
    id: 2,
    date: new Date(),
  },
  {
    id: 3,
    date: new Date(),
  },
  {
    id: 4,
    date: new Date(),
  },
];

function MockInterview() {
  const [questionsPanelIsVisible, setQuestionsPanelIsVisible] = useState(false);
  const [timerIsRunning, setTimerIsRunning] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [currentTab, setCurrentTab] = useState(tabs[0]);
  const [currentAttemptId, setCurrentAttemptId] = useState(1);

  const showQuestionsSidePanelHandler = () => {
    setQuestionsPanelIsVisible(true);
  };

  const hideQuestionsSidePanelHandler = () => {
    setQuestionsPanelIsVisible(false);
  };

  const startRecordingHandler = () => {
    setTimerIsRunning(true);
  };

  const stopRecordingHandler = () => {
    setTimerIsRunning(false);
  };

  const gotToNextQuestion = () => {
    setCurrentQuestion((prevQuestion) => {
      return prevQuestion + 1;
    });
  };

  const goToPreviousQuestion = () => {
    setCurrentQuestion((prevQuestion) => {
      return prevQuestion - 1;
    });
  };

  const changeQuestionHandler = (questionNumber) => {
    setCurrentQuestion(questionNumber);
  };

  const tabChangeHandler = (tab) => {
    setCurrentTab(tab);
  };

  const attemptChangeHandler = (attemptId) => {
    setCurrentAttemptId(attemptId);
  };

  return (
    <div className="flex h-full">
      <QuestionsPanel
        onClose={hideQuestionsSidePanelHandler}
        show={questionsPanelIsVisible}
        currentQuestion={currentQuestion}
        questions={questions}
        onChangeQuestion={changeQuestionHandler}
      />
      <div className="p-8 flex flex-grow">
        {/* <button
          onClick={showQuestionsSidePanelHandler}
          className="bg-[#256bd4] px-4 py-2 rounded-md text-sm"
        >
          All Questions
        </button> */}

        <div className="w-[40%] space-y-8 mr-24">
          <Tabs
            tabs={tabs}
            onTabClick={tabChangeHandler}
            currentTab={currentTab}
          />
          <div className="flex justify-between">
            <button
              disabled={currentQuestion == 1}
              onClick={goToPreviousQuestion}
              className="text-sm rounded-md px-4 py-2 bg-[#256bd4] hover:bg-tertiaryBlue-100"
            >
              Previous
            </button>
            <button
              disabled={currentQuestion == questions?.length}
              onClick={gotToNextQuestion}
              className="text-sm rounded-md px-4 py-2 bg-[#256bd4] hover:bg-tertiaryBlue-100"
            >
              Next
            </button>
          </div>
          {currentTab == tabs[0] && (
            <Question
              currentQuestion={currentQuestion}
              question={questions[currentQuestion - 1]}
            />
          )}
          {currentTab == tabs[1] && (
            <AttemptHistory
              attempts={attempts}
              onAttemptClick={attemptChangeHandler}
              currentAttemptId={currentAttemptId}
            />
          )}
        </div>

        {currentTab == tabs[0] && (
          <div className="w-[600px] space-y-4">
            <Timer timerIsRunning={timerIsRunning} duration={300} />
            <VideoRecorder
              onStartRecording={startRecordingHandler}
              onStopRecording={stopRecordingHandler}
            />
          </div>
        )}
        {currentTab == tabs[1] && (
          <div className="w-[60%]">
            <PreviousAttemptSummary />
          </div>
        )}
      </div>
    </div>
  );
}

export default MockInterview;
