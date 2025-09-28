import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv

# เพิ่ม import สำหรับ Gemini
import os
from google.generativeai import GenerativeModel, configure

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        # กำหนดค่า Gemini API Key
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY not found in environment variables")
        configure(api_key=gemini_api_key)
        self.gemini = GenerativeModel("gemini-2.5-flash")

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Gemini and available tools"""
        messages = [
            {
                "role": "user",
                "parts": [query]
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            # "input_schema": tool.inputSchema
        } for tool in response.tools]

        # เรียก Gemini API
        gemini_response = self.gemini.generate_content(
            contents=messages,
            tools=available_tools,
            generation_config={"max_output_tokens": 1000}
        )

        tool_results = []
        final_text = []

        for part in gemini_response.candidates[0].content.parts:
            if part.get("text"):
                final_text.append(part["text"])
            elif part.get("tool_use"):
                tool_use = part["tool_use"]
                tool_name = tool_use["name"]
                tool_args = tool_use.get("input", {})

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # ส่งผลลัพธ์กลับเข้า Gemini ต่อ
                messages.append({
                    "role": "model",
                    "parts": [part]
                })
                messages.append({
                    "role": "user",
                    "parts": [result.content]
                })

                gemini_response = self.gemini.generate_content(
                    contents=messages,
                    generation_config={"max_output_tokens": 1000}
                )
                # ตอบกลับรอบถัดไป
                if gemini_response.candidates and gemini_response.candidates[0].content.parts:
                    final_text.append(gemini_response.candidates[0].content.parts[0].get("text", ""))

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())