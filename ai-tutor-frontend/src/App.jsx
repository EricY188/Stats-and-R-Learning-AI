import { ChakraProvider, Box, VStack } from "@chakra-ui/react";
import ChatWindow from "./ChatWindow";

function App() {
  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" p={4}>
        <VStack spacing={4} maxW="800px" mx="auto">
          <ChatWindow />
        </VStack>
      </Box>
    </ChakraProvider>
  );
}
export default App;
