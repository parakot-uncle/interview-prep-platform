"use client";

import VideoRecorder from "@/components/mock-interview/VideoRecorder";
import QuestionsPanel from "@/components/mock-interview/QuestionsPanel";
import { useEffect, useState } from "react";
import questions from "@/data/questions.json";
import Timer from "@/components/common/Timer";
import Tabs from "@/components/common/Tabs";
import Question from "@/components/mock-interview/Question";
import PreviousAttemptSummary from "@/components/mock-interview/PreviousAttemptSummary";
import AttemptHistory from "@/components/mock-interview/AttemptHistory";
import axios from "axios";
import { flattenResults } from "@/utils/edit-results";

const tabs = ["Question", "Previous Attempts"];

function MockInterview() {
  const [questionsPanelIsVisible, setQuestionsPanelIsVisible] = useState(false);
  const [timerIsRunning, setTimerIsRunning] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [currentTab, setCurrentTab] = useState(tabs[0]);
  const [currentAttemptId, setCurrentAttemptId] = useState(0);
  const [attemptsHistory, setAttemptsHistory] = useState([]);

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

  const fetchAttemptsHistory = async () => {
    try {
      const res = await axios.get(
        "http://localhost:5000/mock-interview-attempts",
        {
          params: {
            user_id: "6553a5289f33c7101f5ee3b4",
            question: currentQuestion,
          },
        }
      );
      const flattenedResults = res?.data?.map((result) => {
        return flattenResults(result);
      });
      setAttemptsHistory(flattenedResults);
      flattenedResults?.length > 0 &&
        setCurrentAttemptId(flattenedResults[0]?._id);
    } catch (error) {
      console.error(error);
    }
  };

  const submitAttemptHandler = async (videoBlob) => {
    const formData = new FormData();
    formData.append("video", videoBlob);
    formData.append("user", "6553a5289f33c7101f5ee3b4");
    formData.append("question", currentQuestion);

    const res = await axios.post(
      "http://localhost:5000/mock-interview-attempts",
      formData
    );
  };

  useEffect(() => {
    currentTab == tabs[1] && fetchAttemptsHistory();
  }, [currentTab, currentQuestion]);

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
              attempts={attemptsHistory}
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
              onSubmitAttempt={submitAttemptHandler}
            />
          </div>
        )}
        {currentTab == tabs[1] && (
          <div className="w-[60%]">
            <PreviousAttemptSummary
              attempt={attemptsHistory?.find((attempt) => {
                return attempt?._id == currentAttemptId;
              })}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default MockInterview;
