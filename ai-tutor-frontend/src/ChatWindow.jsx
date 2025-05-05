import { useState } from "react";
import {
  Box, Input, Button, Text, Spinner, VStack, HStack,
} from "@chakra-ui/react";
import axios from "axios";

export default function ChatWindow() {
  const [log, setLog] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!text.trim()) return;
    const q = text;
    setLog(l => [...l, { role: "user", content: q }]);
    setText("");
    setLoading(true);
    try {
      const { data } = await axios.post("/api/query/", { question: q });
      setLog(l => [...l, {
        role: "assistant",
        content: data.answer + "\n\n**Next:** " + data.next_step,
      }]);
    } catch (e) {
      setLog(l => [...l, { role: "assistant", content: "Err: " + e.message }]);
    }
    setLoading(false);
  };

  return (
    <VStack w="100%">
      <Box w="100%" h="60vh" overflowY="auto" p={4} bg="white" border="1px solid #eee">
        {log.map((m, i) => (
          <Box key={i} mb={3} bg={m.role === "user" ? "blue.50" : "gray.100"} p={2} borderRadius="md">
            <Text whiteSpace="pre-wrap">{m.content}</Text>
          </Box>
        ))}
        {loading && <Spinner />}
      </Box>
      <HStack w="100%">
        <Input value={text} onChange={e => setText(e.target.value)}
               onKeyDown={e => e.key === "Enter" && send()} placeholder="Ask about stats or R..." />
        <Button onClick={send}>Send</Button>
      </HStack>
    </VStack>
  );
}
