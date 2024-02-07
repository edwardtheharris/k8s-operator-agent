"use client";

import React, { useRef, useState } from "react";
import { RemoteRunnable } from "@langchain/core/runnables/remote";
import * as jsonpatch from "@langchain/core/utils/json_patch";

import { EmptyState } from "../components/EmptyState";
import { ChatMessageBubble, Message } from "../components/ChatMessageBubble";
import { AutoResizeTextarea } from "./AutoResizeTextarea";
import { marked } from "marked";
import { Renderer } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/gradient-dark.css";

import "react-toastify/dist/ReactToastify.css";
import {
  Heading,
  Flex,
  IconButton,
  InputGroup,
  InputRightElement,
  Spinner,
} from "@chakra-ui/react";
import { ArrowUpIcon } from "@chakra-ui/icons";
import { Link } from "@chakra-ui/react";
import { Source } from "./SourceBubble";
import { apiBaseUrl } from "../utils/constants";

export function ChatWindow(props: { conversationId: string }) {
  const conversationId = props.conversationId;

  const messageContainerRef = useRef<HTMLDivElement | null>(null);
  const [messages, setMessages] = useState<Array<Message>>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [chatHistory, setChatHistory] = useState<
    { human: string; ai: string }[]
  >([]);

  const sendMessage = async (message?: string) => {
    if (messageContainerRef.current) {
      messageContainerRef.current.classList.add("grow");
    }
    if (isLoading) {
      return;
    }
    const messageValue = message ?? input;
    if (messageValue === "") return;
    setInput("");
    setMessages((prevMessages) => [
      ...prevMessages,
      { id: Math.random().toString(), content: messageValue, role: "user" },
    ]);
    setIsLoading(true);

    let accumulatedMessage = "";
    let runId: string | undefined = undefined;
    let sources: Source[] | undefined = undefined;
    let messageIndex: number | null = null;

    let renderer = new Renderer();
    renderer.paragraph = (text) => {
      return text + "\n";
    };
    renderer.list = (text) => {
      return `${text}\n\n`;
    };
    renderer.listitem = (text) => {
      return `\n• ${text}`;
    };
    renderer.code = (code, language) => {
      const validLanguage = hljs.getLanguage(language || "")
        ? language
        : "plaintext";
      const highlightedCode = hljs.highlight(
        validLanguage || "plaintext",
        code,
      ).value;
      return `<pre class="highlight bg-gray-700" style="padding: 5px; border-radius: 5px; overflow: auto; overflow-wrap: anywhere; white-space: pre-wrap; max-width: 100%; display: block; line-height: 1.2"><code class="${language}" style="color: #d6e2ef; font-size: 12px; ">${highlightedCode}</code></pre>`;
    };
    marked.setOptions({ renderer });
    try {
      const sourceStepName = "FindDocs";
      let streamedResponse: Record<string, any> = {};
      const remoteChain = new RemoteRunnable({
        url: apiBaseUrl,
        options: {
          timeout: 60000,
        },
      });
      const streamLog = await remoteChain.streamLog(
        {
          input: messageValue,
          chat_history: chatHistory,
        },
        {
          metadata: {
            conversation_id: conversationId,
          },
        }
      );
      for await (const chunk of streamLog) {
        console.log(JSON.stringify(chunk));
        streamedResponse = jsonpatch.applyPatch(streamedResponse, chunk.ops).newDocument;
        if (
          Array.isArray(
            streamedResponse?.logs?.[sourceStepName]?.final_output?.output,
          )
        ) {
          sources = streamedResponse.logs[
            sourceStepName
          ].final_output.output.map((doc: Record<string, any>) => ({
            url: doc.metadata.source,
            title: doc.metadata.title,
          }));
        }
        if (streamedResponse.id !== undefined) {
          runId = streamedResponse.id;
        }
        if (Array.isArray(streamedResponse?.streamed_output)) {
          accumulatedMessage = streamedResponse.streamed_output.join("");
        }
        const parsedResult = marked.parse(accumulatedMessage);

        setMessages((prevMessages) => {
          let newMessages = [...prevMessages];
          if (
            messageIndex === null ||
            newMessages[messageIndex] === undefined
          ) {
            messageIndex = newMessages.length;
            newMessages.push({
              id: Math.random().toString(),
              content: parsedResult.trim(),
              runId: runId,
              sources: sources,
              role: "assistant",
            });
          } else if (newMessages[messageIndex] !== undefined) {
            newMessages[messageIndex].content = parsedResult.trim();
            newMessages[messageIndex].runId = runId;
            newMessages[messageIndex].sources = sources;
          }
          return newMessages;
        });
      }
      setChatHistory((prevChatHistory) => [
        ...prevChatHistory,
        { human: messageValue, ai: accumulatedMessage },
      ]);
      setIsLoading(false);
    } catch (e) {
      setMessages((prevMessages) => prevMessages.slice(0, -1));
      setIsLoading(false);
      setInput(messageValue);
      throw e;
    }
  };

  const sendInitialQuestion = async (question: string) => {
    await sendMessage(question);
  };

  return (
    <div className="flex flex-col items-center p-8 rounded grow max-h-full">
      <Flex
        direction={"column"}
        alignItems={"center"}
        marginTop={messages.length > 0 ? "" : "64px"}
      >
        <Heading
          fontSize={messages.length > 0 ? "2xl" : "3xl"}
          fontWeight={"medium"}
          mb={1}
          color={"white"}
        >
          Kubernetes Operator (LLM Agent 1.0.0)
        </Heading>
        {messages.length > 0 ? (
          <Heading fontSize="md" fontWeight={"normal"} mb={1} color={"white"}>
            We appreciate feedback!
          </Heading>
        ) : (
          <Heading
            fontSize="xl"
            fontWeight={"normal"}
            color={"white"}
            marginTop={"10px"}
            textAlign={"center"}
          >
            Ask me anything about LangChain&apos;s{" "}
            <Link href="https://python.langchain.com/" color={"blue.200"}>
              Python documentation!
            </Link>
          </Heading>
        )}
      </Flex>
      <div
        className="flex flex-col-reverse w-full mb-2 overflow-auto"
        ref={messageContainerRef}
      >
        {messages.length > 0 ? (
          [...messages]
            .reverse()
            .map((m, index) => (
              <ChatMessageBubble
                key={m.id}
                message={{ ...m }}
                aiEmoji="🦜"
                isMostRecent={index === 0}
                messageCompleted={!isLoading}
              ></ChatMessageBubble>
            ))
        ) : (
          <EmptyState onChoice={sendInitialQuestion} />
        )}
      </div>
      <InputGroup size="md" alignItems={"center"}>
        <AutoResizeTextarea
          value={input}
          maxRows={5}
          marginRight={"56px"}
          placeholder="Install a grafana instance on the monitoring namespace with a loadbalancer service on port 8088"
          textColor={"white"}
          borderColor={"rgb(58, 58, 61)"}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            } else if (e.key === "Enter" && e.shiftKey) {
              e.preventDefault();
              setInput(input + "\n");
            }
          }}
        />
        <InputRightElement h="full">
          <IconButton
            colorScheme="blue"
            rounded={"full"}
            aria-label="Send"
            icon={isLoading ? <Spinner /> : <ArrowUpIcon />}
            type="submit"
            onClick={(e) => {
              e.preventDefault();
              sendMessage();
            }}
          />
        </InputRightElement>
      </InputGroup>

      {messages.length === 0 ? (
        <footer className="flex justify-center absolute bottom-8">

        </footer>
      ) : (
        ""
      )}
    </div>
  );
}
