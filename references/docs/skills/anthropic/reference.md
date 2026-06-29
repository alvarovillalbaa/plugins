# Using Agent Skills with the API

> Learn how to use Agent Skills to extend Claude's capabilities through the API.

Agent Skills extend Claude's capabilities through organized folders of instructions, scripts, and resources. This guide shows you how to use both pre-built and custom Skills with the Claude API.

<Note>
  For complete API reference including request/response schemas and all parameters, see:

  * [Skill Management API Reference](/en/api/skills/list-skills) - CRUD operations for Skills
  * [Skill Versions API Reference](/en/api/skills/list-skill-versions) - Version management
</Note>

## Quick Links

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="/en/docs/agents-and-tools/agent-skills/quickstart">
    Create your first Skill
  </Card>

  <Card title="Create Custom Skills" icon="hammer" href="/en/docs/agents-and-tools/agent-skills/best-practices">
    Best practices for authoring Skills
  </Card>
</CardGroup>

## Overview

<Note>
  For a deep dive into the architecture and real-world applications of Agent Skills, read our engineering blog: [Equipping agents for the real world with Agent Skills](https://https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills-skills).
</Note>

Skills integrate with the Messages API through the code execution tool. Whether using pre-built Skills managed by Anthropic or custom Skills you've uploaded, the integration shape is identical—both require code execution and use the same `container` structure.

### Using Skills

Skills integrate identically in the Messages API regardless of source. You specify Skills in the `container` parameter with a `skill_id`, `type`, and optional `version`, and they execute in the code execution environment.

**You can use Skills from two sources:**

| Aspect             | Anthropic Skills                           | Custom Skills                                                   |
| ------------------ | ------------------------------------------ | --------------------------------------------------------------- |
| **Type value**     | `anthropic`                                | `custom`                                                        |
| **Skill IDs**      | Short names: `pptx`, `xlsx`, `docx`, `pdf` | Generated: `skill_01AbCdEfGhIjKlMnOpQrStUv`                     |
| **Version format** | Date-based: `20251013` or `latest`         | Epoch timestamp: `1759178010641129` or `latest`                 |
| **Management**     | Pre-built and maintained by Anthropic      | Upload and manage via [Skills API](/en/api/skills/create-skill) |
| **Availability**   | Available to all users                     | Private to your workspace                                       |

Both skill sources are returned by the [List Skills endpoint](/en/api/skills/list-skills) (use the `source` parameter to filter). The integration shape and execution environment are identical—the only difference is where the Skills come from and how they're managed.

### Prerequisites

To use Skills, you need:

1. **Anthropic API key** from the [Console](https://console.anthropic.com/settings/keys)
2. **Beta headers**:
   * `code-execution-2025-08-25` - Enables code execution (required for Skills)
   * `skills-2025-10-02` - Enables Skills API
   * `files-api-2025-04-14` - For uploading/downloading files to/from container
3. **Code execution tool** enabled in your requests

***

## Using Skills in Messages

### Container Parameter

Skills are specified using the `container` parameter in the Messages API. You can include up to 8 Skills per request.

The structure is identical for both Anthropic and custom Skills—specify the required `type` and `skill_id`, and optionally include `version` to pin to a specific version:

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "anthropic",
                  "skill_id": "pptx",
                  "version": "latest"
              }
          ]
      },
      messages=[{
          "role": "user",
          "content": "Create a presentation about renewable energy"
      }],
      tools=[{
          "type": "code_execution_20250825",
          "name": "code_execution"
      }]
  )
  ```

  ```typescript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {
          type: 'anthropic',
          skill_id: 'pptx',
          version: 'latest'
        }
      ]
    },
    messages: [{
      role: 'user',
      content: 'Create a presentation about renewable energy'
    }],
    tools: [{
      type: 'code_execution_20250825',
      name: 'code_execution'
    }]
  });
  ```

  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create a presentation about renewable energy"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```
</CodeGroup>

### Downloading Generated Files

When Skills create documents (Excel, PowerPoint, PDF, Word), they return `file_id` attributes in the response. You must use the Files API to download these files.

**How it works:**

1. Skills create files during code execution
2. Response includes `file_id` for each created file
3. Use Files API to download the actual file content
4. Save locally or process as needed

**Example: Creating and downloading an Excel file**

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  # Step 1: Use a Skill to create a file
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=[{
          "role": "user",
          "content": "Create an Excel file with a simple budget spreadsheet"
      }],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Step 2: Extract file IDs from the response
  def extract_file_ids(response):
      file_ids = []
      for item in response.content:
          if item.type == 'bash_code_execution_tool_result':
              content_item = item.content
              if content_item.type == 'bash_code_execution_result':
                  for file in content_item.content:
                      if hasattr(file, 'file_id'):
                          file_ids.append(file.file_id)
      return file_ids

  # Step 3: Download the file using Files API
  for file_id in extract_file_ids(response):
      file_metadata = client.beta.files.retrieve_metadata(
          file_id=file_id,
          betas=["files-api-2025-04-14"]
      )
      file_content = client.beta.files.download(
          file_id=file_id,
          betas=["files-api-2025-04-14"]
      )

      # Step 4: Save to disk
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const client = new Anthropic();

  // Step 1: Use a Skill to create a file
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages: [{
      role: 'user',
      content: 'Create an Excel file with a simple budget spreadsheet'
    }],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Step 2: Extract file IDs from the response
  function extractFileIds(response: any): string[] {
    const fileIds: string[] = [];
    for (const item of response.content) {
      if (item.type === 'bash_code_execution_tool_result') {
        const contentItem = item.content;
        if (contentItem.type === 'bash_code_execution_result') {
          for (const file of contentItem.content) {
            if ('file_id' in file) {
              fileIds.push(file.file_id);
            }
          }
        }
      }
    }
    return fileIds;
  }

  // Step 3: Download the file using Files API
  const fs = require('fs');
  for (const fileId of extractFileIds(response)) {
    const fileMetadata = await client.beta.files.retrieve_metadata(fileId, {
      betas: ['files-api-2025-04-14']
    });
    const fileContent = await client.beta.files.download(fileId, {
      betas: ['files-api-2025-04-14']
    });

    // Step 4: Save to disk
    fs.writeFileSync(fileMetadata.filename, Buffer.from(await fileContent.arrayBuffer()));
    console.log(`Downloaded: ${fileMetadata.filename}`);
  }
  ```

  ```bash Shell theme={null}
  # Step 1: Use a Skill to create a file
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create an Excel file with a simple budget spreadsheet"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Step 2: Extract file_id from response (using jq)
  FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="bash_code_execution_tool_result") | .content | select(.type=="bash_code_execution_result") | .content[] | select(.file_id) | .file_id')

  # Step 3: Get filename from metadata
  FILENAME=$(curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" | jq -r '.filename')

  # Step 4: Download the file using Files API
  curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    --output "$FILENAME"

  echo "Downloaded: $FILENAME"
  ```
</CodeGroup>

**Additional Files API operations:**

<CodeGroup>
  ```python Python theme={null}
  # Get file metadata
  file_info = client.beta.files.retrieve_metadata(
      file_id=file_id,
      betas=["files-api-2025-04-14"]
  )
  print(f"Filename: {file_info.filename}, Size: {file_info.size_bytes} bytes")

  # List all files
  files = client.beta.files.list(betas=["files-api-2025-04-14"])
  for file in files.data:
      print(f"{file.filename} - {file.created_at}")

  # Delete a file
  client.beta.files.delete(
      file_id=file_id,
      betas=["files-api-2025-04-14"]
  )
  ```

  ```typescript TypeScript theme={null}
  // Get file metadata
  const fileInfo = await client.beta.files.retrieve_metadata(fileId, {
    betas: ['files-api-2025-04-14']
  });
  console.log(`Filename: ${fileInfo.filename}, Size: ${fileInfo.size_bytes} bytes`);

  // List all files
  const files = await client.beta.files.list({
    betas: ['files-api-2025-04-14']
  });
  for (const file of files.data) {
    console.log(`${file.filename} - ${file.created_at}`);
  }

  // Delete a file
  await client.beta.files.delete(fileId, {
    betas: ['files-api-2025-04-14']
  });
  ```

  ```bash Shell theme={null}
  # Get file metadata
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # List all files
  curl "https://api.anthropic.com/v1/files" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # Delete a file
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```
</CodeGroup>

<Note>
  For complete details on the Files API, see the [Files API documentation](/en/api/files-content).
</Note>

### Multi-Turn Conversations

Reuse the same container across multiple messages by specifying the container ID:

<CodeGroup>
  ```python Python theme={null}
  # First request creates container
  response1 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=[{"role": "user", "content": "Analyze this sales data"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Continue conversation with same container
  messages = [
      {"role": "user", "content": "Analyze this sales data"},
      {"role": "assistant", "content": response1.content},
      {"role": "user", "content": "What was the total revenue?"}
  ]

  response2 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "id": response1.container.id,  # Reuse container
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // First request creates container
  const response1 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages: [{role: 'user', content: 'Analyze this sales data'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Continue conversation with same container
  const messages = [
    {role: 'user', content: 'Analyze this sales data'},
    {role: 'assistant', content: response1.content},
    {role: 'user', content: 'What was the total revenue?'}
  ];

  const response2 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      id: response1.container.id,  // Reuse container
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages,
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```
</CodeGroup>

### Long-Running Operations

Skills may perform operations that require multiple turns. Handle `pause_turn` stop reasons:

<CodeGroup>
  ```python Python theme={null}
  messages = [{"role": "user", "content": "Process this large dataset"}]
  max_retries = 10

  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
          ]
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Handle pause_turn for long operations
  for i in range(max_retries):
      if response.stop_reason != "pause_turn":
          break

      messages.append({"role": "assistant", "content": response.content})
      response = client.beta.messages.create(
          model="claude-sonnet-4-5-20250929",
          max_tokens=4096,
          betas=["code-execution-2025-08-25", "skills-2025-10-02"],
          container={
              "id": response.container.id,
              "skills": [
                  {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
              ]
          },
          messages=messages,
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
      )
  ```

  ```typescript TypeScript theme={null}
  let messages = [{role: 'user' as const, content: 'Process this large dataset'}];
  const maxRetries = 10;

  let response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'custom', skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv', version: 'latest'}
      ]
    },
    messages,
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Handle pause_turn for long operations
  for (let i = 0; i < maxRetries; i++) {
    if (response.stop_reason !== 'pause_turn') {
      break;
    }

    messages.push({role: 'assistant', content: response.content});
    response = await client.beta.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: {
        id: response.container.id,
        skills: [
          {type: 'custom', skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv', version: 'latest'}
        ]
      },
      messages,
      tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
    });
  }
  ```

  ```bash Shell theme={null}
  # Initial request
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Process this large dataset"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Check stop_reason and handle pause_turn in a loop
  STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.container.id')

  while [ "$STOP_REASON" = "pause_turn" ]; do
    # Continue with same container
    RESPONSE=$(curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
      -H "content-type: application/json" \
      -d "{
        \"model\": \"claude-sonnet-4-5-20250929\",
        \"max_tokens\": 4096,
        \"container\": {
          \"id\": \"$CONTAINER_ID\",
          \"skills\": [{
            \"type\": \"custom\",
            \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
            \"version\": \"latest\"
          }]
        },
        \"messages\": [/* include conversation history */],
        \"tools\": [{
          \"type\": \"code_execution_20250825\",
          \"name\": \"code_execution\"
        }]
      }")

    STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  done
  ```
</CodeGroup>

<Note>
  The response may include a `pause_turn` stop reason, which indicates that the API paused a long-running Skill operation. You can provide the response back as-is in a subsequent request to let Claude continue its turn, or modify the content if you wish to interrupt the conversation and provide additional guidance.
</Note>

### Using Multiple Skills

Combine multiple Skills in a single request to handle complex workflows:

<CodeGroup>
  ```python Python theme={null}
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "anthropic",
                  "skill_id": "xlsx",
                  "version": "latest"
              },
              {
                  "type": "anthropic",
                  "skill_id": "pptx",
                  "version": "latest"
              },
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest"
              }
          ]
      },
      messages=[{
          "role": "user",
          "content": "Analyze sales data and create a presentation"
      }],
      tools=[{
          "type": "code_execution_20250825",
          "name": "code_execution"
      }]
  )
  ```

  ```typescript TypeScript theme={null}
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {
          type: 'anthropic',
          skill_id: 'xlsx',
          version: 'latest'
        },
        {
          type: 'anthropic',
          skill_id: 'pptx',
          version: 'latest'
        },
        {
          type: 'custom',
          skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          version: 'latest'
        }
      ]
    },
    messages: [{
      role: 'user',
      content: 'Analyze sales data and create a presentation'
    }],
    tools: [{
      type: 'code_execution_20250825',
      name: 'code_execution'
    }]
  });
  ```

  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "xlsx",
            "version": "latest"
          },
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          },
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Analyze sales data and create a presentation"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```
</CodeGroup>

***

## Managing Custom Skills

### Creating a Skill

Upload your custom Skill to make it available in your workspace. You can upload using either a directory path or individual file objects.

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  # Option 1: Using files_from_dir helper (Python only, recommended)
  from anthropic.lib import files_from_dir

  skill = client.beta.skills.create(
      display_title="Financial Analysis",
      files=files_from_dir("/path/to/financial_analysis_skill"),
      betas=["skills-2025-10-02"]
  )

  # Option 2: Using a zip file
  skill = client.beta.skills.create(
      display_title="Financial Analysis",
      files=[("skill.zip", open("financial_analysis_skill.zip", "rb"))],
      betas=["skills-2025-10-02"]
  )

  # Option 3: Using file tuples (filename, file_content, mime_type)
  skill = client.beta.skills.create(
      display_title="Financial Analysis",
      files=[
          ("financial_skill/SKILL.md", open("financial_skill/SKILL.md", "rb"), "text/markdown"),
          ("financial_skill/analyze.py", open("financial_skill/analyze.py", "rb"), "text/x-python"),
      ],
      betas=["skills-2025-10-02"]
  )

  print(f"Created skill: {skill.id}")
  print(f"Latest version: {skill.latest_version}")
  ```

  ```typescript TypeScript theme={null}
  import Anthropic, { toFile } from '@anthropic-ai/sdk';
  import fs from 'fs';

  const client = new Anthropic();

  // Option 1: Using a zip file
  const skill = await client.beta.skills.create({
    displayTitle: 'Financial Analysis',
    files: [
      await toFile(
        fs.createReadStream('financial_analysis_skill.zip'),
        'skill.zip'
      )
    ],
    betas: ['skills-2025-10-02']
  });

  // Option 2: Using individual file objects
  const skill = await client.beta.skills.create({
    displayTitle: 'Financial Analysis',
    files: [
      await toFile(
        fs.createReadStream('financial_skill/SKILL.md'),
        'financial_skill/SKILL.md',
        { type: 'text/markdown' }
      ),
      await toFile(
        fs.createReadStream('financial_skill/analyze.py'),
        'financial_skill/analyze.py',
        { type: 'text/x-python' }
      ),
    ],
    betas: ['skills-2025-10-02']
  });

  console.log(`Created skill: ${skill.id}`);
  console.log(`Latest version: ${skill.latest_version}`);
  ```

  ```bash Shell theme={null}
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "display_title=Financial Analysis" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
  ```
</CodeGroup>

**Requirements:**

* Must include a SKILL.md file at the top level
* All files must specify a common root directory in their paths
* Total upload size must be under 8MB
* YAML frontmatter requirements:
  * `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
  * `description`: Maximum 1024 characters, non-empty, no XML tags

For complete request/response schemas, see the [Create Skill API reference](/en/api/skills/create-skill).

### Listing Skills

Retrieve all Skills available to your workspace, including both Anthropic pre-built Skills and your custom Skills. Use the `source` parameter to filter by skill type:

<CodeGroup>
  ```python Python theme={null}
  # List all Skills
  skills = client.beta.skills.list(
      betas=["skills-2025-10-02"]
  )

  for skill in skills.data:
      print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

  # List only custom Skills
  custom_skills = client.beta.skills.list(
      source="custom",
      betas=["skills-2025-10-02"]
  )
  ```

  ```typescript TypeScript theme={null}
  // List all Skills
  const skills = await client.beta.skills.list({
    betas: ['skills-2025-10-02']
  });

  for (const skill of skills.data) {
    console.log(`${skill.id}: ${skill.display_title} (source: ${skill.source})`);
  }

  // List only custom Skills
  const customSkills = await client.beta.skills.list({
    source: 'custom',
    betas: ['skills-2025-10-02']
  });
  ```

  ```bash Shell theme={null}
  # List all Skills
  curl "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"

  # List only custom Skills
  curl "https://api.anthropic.com/v1/skills?source=custom" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```
</CodeGroup>

See the [List Skills API reference](/en/api/skills/list-skills) for pagination and filtering options.

### Retrieving a Skill

Get details about a specific Skill:

<CodeGroup>
  ```python Python theme={null}
  skill = client.beta.skills.retrieve(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      betas=["skills-2025-10-02"]
  )

  print(f"Skill: {skill.display_title}")
  print(f"Latest version: {skill.latest_version}")
  print(f"Created: {skill.created_at}")
  ```

  ```typescript TypeScript theme={null}
  const skill = await client.beta.skills.retrieve(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    { betas: ['skills-2025-10-02'] }
  );

  console.log(`Skill: ${skill.display_title}`);
  console.log(`Latest version: ${skill.latest_version}`);
  console.log(`Created: ${skill.created_at}`);
  ```

  ```bash Shell theme={null}
  curl "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```
</CodeGroup>

### Deleting a Skill

To delete a Skill, you must first delete all its versions:

<CodeGroup>
  ```python Python theme={null}
  # Step 1: Delete all versions
  versions = client.beta.skills.versions.list(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      betas=["skills-2025-10-02"]
  )

  for version in versions.data:
      client.beta.skills.versions.delete(
          skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
          version=version.version,
          betas=["skills-2025-10-02"]
      )

  # Step 2: Delete the Skill
  client.beta.skills.delete(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      betas=["skills-2025-10-02"]
  )
  ```

  ```typescript TypeScript theme={null}
  // Step 1: Delete all versions
  const versions = await client.beta.skills.versions.list(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    { betas: ['skills-2025-10-02'] }
  );

  for (const version of versions.data) {
    await client.beta.skills.versions.delete(
      'skill_01AbCdEfGhIjKlMnOpQrStUv',
      version.version,
      { betas: ['skills-2025-10-02'] }
    );
  }

  // Step 2: Delete the Skill
  await client.beta.skills.delete(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    { betas: ['skills-2025-10-02'] }
  );
  ```

  ```bash Shell theme={null}
  # Delete all versions first, then delete the Skill
  curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```
</CodeGroup>

Attempting to delete a Skill with existing versions will return a 400 error.

### Versioning

Skills support versioning to manage updates safely:

**Anthropic-Managed Skills**:

* Versions use date format: `20251013`
* New versions released as updates are made
* Specify exact versions for stability

**Custom Skills**:

* Auto-generated epoch timestamps: `1759178010641129`
* Use `"latest"` to always get the most recent version
* Create new versions when updating Skill files

<CodeGroup>
  ```python Python theme={null}
  # Create a new version
  from anthropic.lib import files_from_dir

  new_version = client.beta.skills.versions.create(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      files=files_from_dir("/path/to/updated_skill"),
      betas=["skills-2025-10-02"]
  )

  # Use specific version
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": new_version.version
          }]
      },
      messages=[{"role": "user", "content": "Use updated Skill"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Use latest version
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "latest"
          }]
      },
      messages=[{"role": "user", "content": "Use latest Skill version"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // Create a new version using a zip file
  const fs = require('fs');

  const newVersion = await client.beta.skills.versions.create(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    {
      files: [
        fs.createReadStream('updated_skill.zip')
      ],
      betas: ['skills-2025-10-02']
    }
  );

  // Use specific version
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [{
        type: 'custom',
        skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
        version: newVersion.version
      }]
    },
    messages: [{role: 'user', content: 'Use updated Skill'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Use latest version
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [{
        type: 'custom',
        skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
        version: 'latest'
      }]
    },
    messages: [{role: 'user', content: 'Use latest Skill version'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```

  ```bash Shell theme={null}
  # Create a new version
  NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@updated_skill/SKILL.md;filename=updated_skill/SKILL.md")

  VERSION_NUMBER=$(echo "$NEW_VERSION" | jq -r '.version')

  # Use specific version
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-sonnet-4-5-20250929\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"$VERSION_NUMBER\"
        }]
      },
      \"messages\": [{\"role\": \"user\", \"content\": \"Use updated Skill\"}],
      \"tools\": [{\"type\": \"code_execution_20250825\", \"name\": \"code_execution\"}]
    }"

  # Use latest version
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }]
      },
      "messages": [{"role": "user", "content": "Use latest Skill version"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```
</CodeGroup>

See the [Create Skill Version API reference](/en/api/skills/create-skill-version) for complete details.

***

## How Skills Are Loaded

When you specify Skills in a container:

1. **Metadata Discovery**: Claude sees metadata for each Skill (name, description) in the system prompt
2. **File Loading**: Skill files are copied into the container at `/skills/{directory}/`
3. **Automatic Use**: Claude automatically loads and uses Skills when relevant to your request
4. **Composition**: Multiple Skills compose together for complex workflows

The progressive disclosure architecture ensures efficient context usage—Claude only loads full Skill instructions when needed.

***

## Use Cases

### Organizational Skills

**Brand & Communications**

* Apply company-specific formatting (colors, fonts, layouts) to documents
* Generate communications following organizational templates
* Ensure consistent brand guidelines across all outputs

**Project Management**

* Structure notes with company-specific formats (OKRs, decision logs)
* Generate tasks following team conventions
* Create standardized meeting recaps and status updates

**Business Operations**

* Create company-standard reports, proposals, and analyses
* Execute company-specific analytical procedures
* Generate financial models following organizational templates

### Personal Skills

**Content Creation**

* Custom document templates
* Specialized formatting and styling
* Domain-specific content generation

**Data Analysis**

* Custom data processing pipelines
* Specialized visualization templates
* Industry-specific analytical methods

**Development & Automation**

* Code generation templates
* Testing frameworks
* Deployment workflows

### Example: Financial Modeling

Combine Excel and custom DCF analysis Skills:

<CodeGroup>
  ```python Python theme={null}
  # Create custom DCF analysis Skill
  from anthropic.lib import files_from_dir

  dcf_skill = client.beta.skills.create(
      display_title="DCF Analysis",
      files=files_from_dir("/path/to/dcf_skill"),
      betas=["skills-2025-10-02"]
  )

  # Use with Excel to create financial model
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "custom", "skill_id": dcf_skill.id, "version": "latest"}
          ]
      },
      messages=[{
          "role": "user",
          "content": "Build a DCF valuation model for a SaaS company with the attached financials"
      }],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // Create custom DCF analysis Skill
  import { toFile } from '@anthropic-ai/sdk';
  import fs from 'fs';

  const dcfSkill = await client.beta.skills.create({
    displayTitle: 'DCF Analysis',
    files: [
      await toFile(fs.createReadStream('dcf_skill.zip'), 'skill.zip')
    ],
    betas: ['skills-2025-10-02']
  });

  // Use with Excel to create financial model
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'},
        {type: 'custom', skill_id: dcfSkill.id, version: 'latest'}
      ]
    },
    messages: [{
      role: 'user',
      content: 'Build a DCF valuation model for a SaaS company with the attached financials'
    }],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```

  ```bash Shell theme={null}
  # Create custom DCF analysis Skill
  DCF_SKILL=$(curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "display_title=DCF Analysis" \
    -F "files[]=@dcf_skill/SKILL.md;filename=dcf_skill/SKILL.md")

  DCF_SKILL_ID=$(echo "$DCF_SKILL" | jq -r '.id')

  # Use with Excel to create financial model
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-sonnet-4-5-20250929\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [
          {
            \"type\": \"anthropic\",
            \"skill_id\": \"xlsx\",
            \"version\": \"latest\"
          },
          {
            \"type\": \"custom\",
            \"skill_id\": \"$DCF_SKILL_ID\",
            \"version\": \"latest\"
          }
        ]
      },
      \"messages\": [{
        \"role\": \"user\",
        \"content\": \"Build a DCF valuation model for a SaaS company with the attached financials\"
      }],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }"
  ```
</CodeGroup>

***

## Limits and Constraints

### Request Limits

* **Maximum Skills per request**: 8
* **Maximum Skill upload size**: 8MB (all files combined)
* **YAML frontmatter requirements**:
  * `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words
  * `description`: Maximum 1024 characters, non-empty, no XML tags

### Environment Constraints

Skills run in the code execution container with these limitations:

* **No network access** - Cannot make external API calls
* **No runtime package installation** - Only pre-installed packages available
* **Isolated environment** - Each request gets a fresh container

See the [code execution tool documentation](/en/docs/agents-and-tools/tool-use/code-execution-tool) for available packages.

***

## Best Practices

### When to Use Multiple Skills

Combine Skills when tasks involve multiple document types or domains:

**Good use cases:**

* Data analysis (Excel) + presentation creation (PowerPoint)
* Report generation (Word) + export to PDF
* Custom domain logic + document generation

**Avoid:**

* Including unused Skills (impacts performance)

### Version Management Strategy

**For production:**

```python  theme={null}
# Pin to specific versions for stability
container={
    "skills": [{
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "1759178010641129"  # Specific version
    }]
}
```

**For development:**

```python  theme={null}
# Use latest for active development
container={
    "skills": [{
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "latest"  # Always get newest
    }]
}
```

### Prompt Caching Considerations

When using prompt caching, note that changing the Skills list in your container will break the cache:

<CodeGroup>
  ```python Python theme={null}
  # First request creates cache
  response1 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=[{"role": "user", "content": "Analyze sales data"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Adding/removing Skills breaks cache
  response2 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "anthropic", "skill_id": "pptx", "version": "latest"}  # Cache miss
          ]
      },
      messages=[{"role": "user", "content": "Create a presentation"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // First request creates cache
  const response1 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02', 'prompt-caching-2024-07-31'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages: [{role: 'user', content: 'Analyze sales data'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Adding/removing Skills breaks cache
  const response2 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02', 'prompt-caching-2024-07-31'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'},
        {type: 'anthropic', skill_id: 'pptx', version: 'latest'}  // Cache miss
      ]
    },
    messages: [{role: 'user', content: 'Create a presentation'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```

  ```bash Shell theme={null}
  # First request creates cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Analyze sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'

  # Adding/removing Skills breaks cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
          {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Create a presentation"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```
</CodeGroup>

For best caching performance, keep your Skills list consistent across requests.

### Error Handling

Handle Skill-related errors gracefully:

<CodeGroup>
  ```python Python theme={null}
  try:
      response = client.beta.messages.create(
          model="claude-sonnet-4-5-20250929",
          max_tokens=4096,
          betas=["code-execution-2025-08-25", "skills-2025-10-02"],
          container={
              "skills": [
                  {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
              ]
          },
          messages=[{"role": "user", "content": "Process data"}],
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
      )
  except anthropic.BadRequestError as e:
      if "skill" in str(e):
          print(f"Skill error: {e}")
          # Handle skill-specific errors
      else:
          raise
  ```

  ```typescript TypeScript theme={null}
  try {
    const response = await client.beta.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: {
        skills: [
          {type: 'custom', skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv', version: 'latest'}
        ]
      },
      messages: [{role: 'user', content: 'Process data'}],
      tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
    });
  } catch (error) {
    if (error instanceof Anthropic.BadRequestError && error.message.includes('skill')) {
      console.error(`Skill error: ${error.message}`);
      // Handle skill-specific errors
    } else {
      throw error;
    }
  }
  ```
</CodeGroup>

***

## Next Steps

<CardGroup cols={2}>
  <Card title="API Reference" icon="book" href="/en/api/skills/create-skill">
    Complete API reference with all endpoints
  </Card>

  <Card title="Authoring Guide" icon="pen" href="/en/docs/agents-and-tools/agent-skills/best-practices">
    Best practices for writing effective Skills
  </Card>

  <Card title="Code Execution Tool" icon="terminal" href="/en/docs/agents-and-tools/tool-use/code-execution-tool">
    Learn about the code execution environment
  </Card>
</CardGroup>

# Using Agent Skills with the API

> Learn how to use Agent Skills to extend Claude's capabilities through the API.

Agent Skills extend Claude's capabilities through organized folders of instructions, scripts, and resources. This guide shows you how to use both pre-built and custom Skills with the Claude API.

<Note>
  For complete API reference including request/response schemas and all parameters, see:

  * [Skill Management API Reference](/en/api/skills/list-skills) - CRUD operations for Skills
  * [Skill Versions API Reference](/en/api/skills/list-skill-versions) - Version management
</Note>

## Quick Links

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills" icon="rocket" href="/en/docs/agents-and-tools/agent-skills/quickstart">
    Create your first Skill
  </Card>

  <Card title="Create Custom Skills" icon="hammer" href="/en/docs/agents-and-tools/agent-skills/best-practices">
    Best practices for authoring Skills
  </Card>
</CardGroup>

## Overview

<Note>
  For a deep dive into the architecture and real-world applications of Agent Skills, read our engineering blog: [Equipping agents for the real world with Agent Skills](https://https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills-skills).
</Note>

Skills integrate with the Messages API through the code execution tool. Whether using pre-built Skills managed by Anthropic or custom Skills you've uploaded, the integration shape is identical—both require code execution and use the same `container` structure.

### Using Skills

Skills integrate identically in the Messages API regardless of source. You specify Skills in the `container` parameter with a `skill_id`, `type`, and optional `version`, and they execute in the code execution environment.

**You can use Skills from two sources:**

| Aspect             | Anthropic Skills                           | Custom Skills                                                   |
| ------------------ | ------------------------------------------ | --------------------------------------------------------------- |
| **Type value**     | `anthropic`                                | `custom`                                                        |
| **Skill IDs**      | Short names: `pptx`, `xlsx`, `docx`, `pdf` | Generated: `skill_01AbCdEfGhIjKlMnOpQrStUv`                     |
| **Version format** | Date-based: `20251013` or `latest`         | Epoch timestamp: `1759178010641129` or `latest`                 |
| **Management**     | Pre-built and maintained by Anthropic      | Upload and manage via [Skills API](/en/api/skills/create-skill) |
| **Availability**   | Available to all users                     | Private to your workspace                                       |

Both skill sources are returned by the [List Skills endpoint](/en/api/skills/list-skills) (use the `source` parameter to filter). The integration shape and execution environment are identical—the only difference is where the Skills come from and how they're managed.

### Prerequisites

To use Skills, you need:

1. **Anthropic API key** from the [Console](https://console.anthropic.com/settings/keys)
2. **Beta headers**:
   * `code-execution-2025-08-25` - Enables code execution (required for Skills)
   * `skills-2025-10-02` - Enables Skills API
   * `files-api-2025-04-14` - For uploading/downloading files to/from container
3. **Code execution tool** enabled in your requests

***

## Using Skills in Messages

### Container Parameter

Skills are specified using the `container` parameter in the Messages API. You can include up to 8 Skills per request.

The structure is identical for both Anthropic and custom Skills—specify the required `type` and `skill_id`, and optionally include `version` to pin to a specific version:

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "anthropic",
                  "skill_id": "pptx",
                  "version": "latest"
              }
          ]
      },
      messages=[{
          "role": "user",
          "content": "Create a presentation about renewable energy"
      }],
      tools=[{
          "type": "code_execution_20250825",
          "name": "code_execution"
      }]
  )
  ```

  ```typescript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {
          type: 'anthropic',
          skill_id: 'pptx',
          version: 'latest'
        }
      ]
    },
    messages: [{
      role: 'user',
      content: 'Create a presentation about renewable energy'
    }],
    tools: [{
      type: 'code_execution_20250825',
      name: 'code_execution'
    }]
  });
  ```

  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create a presentation about renewable energy"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```
</CodeGroup>

### Downloading Generated Files

When Skills create documents (Excel, PowerPoint, PDF, Word), they return `file_id` attributes in the response. You must use the Files API to download these files.

**How it works:**

1. Skills create files during code execution
2. Response includes `file_id` for each created file
3. Use Files API to download the actual file content
4. Save locally or process as needed

**Example: Creating and downloading an Excel file**

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  # Step 1: Use a Skill to create a file
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=[{
          "role": "user",
          "content": "Create an Excel file with a simple budget spreadsheet"
      }],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Step 2: Extract file IDs from the response
  def extract_file_ids(response):
      file_ids = []
      for item in response.content:
          if item.type == 'bash_code_execution_tool_result':
              content_item = item.content
              if content_item.type == 'bash_code_execution_result':
                  for file in content_item.content:
                      if hasattr(file, 'file_id'):
                          file_ids.append(file.file_id)
      return file_ids

  # Step 3: Download the file using Files API
  for file_id in extract_file_ids(response):
      file_metadata = client.beta.files.retrieve_metadata(
          file_id=file_id,
          betas=["files-api-2025-04-14"]
      )
      file_content = client.beta.files.download(
          file_id=file_id,
          betas=["files-api-2025-04-14"]
      )

      # Step 4: Save to disk
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const client = new Anthropic();

  // Step 1: Use a Skill to create a file
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages: [{
      role: 'user',
      content: 'Create an Excel file with a simple budget spreadsheet'
    }],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Step 2: Extract file IDs from the response
  function extractFileIds(response: any): string[] {
    const fileIds: string[] = [];
    for (const item of response.content) {
      if (item.type === 'bash_code_execution_tool_result') {
        const contentItem = item.content;
        if (contentItem.type === 'bash_code_execution_result') {
          for (const file of contentItem.content) {
            if ('file_id' in file) {
              fileIds.push(file.file_id);
            }
          }
        }
      }
    }
    return fileIds;
  }

  // Step 3: Download the file using Files API
  const fs = require('fs');
  for (const fileId of extractFileIds(response)) {
    const fileMetadata = await client.beta.files.retrieve_metadata(fileId, {
      betas: ['files-api-2025-04-14']
    });
    const fileContent = await client.beta.files.download(fileId, {
      betas: ['files-api-2025-04-14']
    });

    // Step 4: Save to disk
    fs.writeFileSync(fileMetadata.filename, Buffer.from(await fileContent.arrayBuffer()));
    console.log(`Downloaded: ${fileMetadata.filename}`);
  }
  ```

  ```bash Shell theme={null}
  # Step 1: Use a Skill to create a file
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create an Excel file with a simple budget spreadsheet"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Step 2: Extract file_id from response (using jq)
  FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="bash_code_execution_tool_result") | .content | select(.type=="bash_code_execution_result") | .content[] | select(.file_id) | .file_id')

  # Step 3: Get filename from metadata
  FILENAME=$(curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" | jq -r '.filename')

  # Step 4: Download the file using Files API
  curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14" \
    --output "$FILENAME"

  echo "Downloaded: $FILENAME"
  ```
</CodeGroup>

**Additional Files API operations:**

<CodeGroup>
  ```python Python theme={null}
  # Get file metadata
  file_info = client.beta.files.retrieve_metadata(
      file_id=file_id,
      betas=["files-api-2025-04-14"]
  )
  print(f"Filename: {file_info.filename}, Size: {file_info.size_bytes} bytes")

  # List all files
  files = client.beta.files.list(betas=["files-api-2025-04-14"])
  for file in files.data:
      print(f"{file.filename} - {file.created_at}")

  # Delete a file
  client.beta.files.delete(
      file_id=file_id,
      betas=["files-api-2025-04-14"]
  )
  ```

  ```typescript TypeScript theme={null}
  // Get file metadata
  const fileInfo = await client.beta.files.retrieve_metadata(fileId, {
    betas: ['files-api-2025-04-14']
  });
  console.log(`Filename: ${fileInfo.filename}, Size: ${fileInfo.size_bytes} bytes`);

  // List all files
  const files = await client.beta.files.list({
    betas: ['files-api-2025-04-14']
  });
  for (const file of files.data) {
    console.log(`${file.filename} - ${file.created_at}`);
  }

  // Delete a file
  await client.beta.files.delete(fileId, {
    betas: ['files-api-2025-04-14']
  });
  ```

  ```bash Shell theme={null}
  # Get file metadata
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # List all files
  curl "https://api.anthropic.com/v1/files" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"

  # Delete a file
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: files-api-2025-04-14"
  ```
</CodeGroup>

<Note>
  For complete details on the Files API, see the [Files API documentation](/en/api/files-content).
</Note>

### Multi-Turn Conversations

Reuse the same container across multiple messages by specifying the container ID:

<CodeGroup>
  ```python Python theme={null}
  # First request creates container
  response1 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=[{"role": "user", "content": "Analyze this sales data"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Continue conversation with same container
  messages = [
      {"role": "user", "content": "Analyze this sales data"},
      {"role": "assistant", "content": response1.content},
      {"role": "user", "content": "What was the total revenue?"}
  ]

  response2 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "id": response1.container.id,  # Reuse container
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // First request creates container
  const response1 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages: [{role: 'user', content: 'Analyze this sales data'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Continue conversation with same container
  const messages = [
    {role: 'user', content: 'Analyze this sales data'},
    {role: 'assistant', content: response1.content},
    {role: 'user', content: 'What was the total revenue?'}
  ];

  const response2 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      id: response1.container.id,  // Reuse container
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages,
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```
</CodeGroup>

### Long-Running Operations

Skills may perform operations that require multiple turns. Handle `pause_turn` stop reasons:

<CodeGroup>
  ```python Python theme={null}
  messages = [{"role": "user", "content": "Process this large dataset"}]
  max_retries = 10

  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
          ]
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Handle pause_turn for long operations
  for i in range(max_retries):
      if response.stop_reason != "pause_turn":
          break

      messages.append({"role": "assistant", "content": response.content})
      response = client.beta.messages.create(
          model="claude-sonnet-4-5-20250929",
          max_tokens=4096,
          betas=["code-execution-2025-08-25", "skills-2025-10-02"],
          container={
              "id": response.container.id,
              "skills": [
                  {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
              ]
          },
          messages=messages,
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
      )
  ```

  ```typescript TypeScript theme={null}
  let messages = [{role: 'user' as const, content: 'Process this large dataset'}];
  const maxRetries = 10;

  let response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'custom', skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv', version: 'latest'}
      ]
    },
    messages,
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Handle pause_turn for long operations
  for (let i = 0; i < maxRetries; i++) {
    if (response.stop_reason !== 'pause_turn') {
      break;
    }

    messages.push({role: 'assistant', content: response.content});
    response = await client.beta.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: {
        id: response.container.id,
        skills: [
          {type: 'custom', skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv', version: 'latest'}
        ]
      },
      messages,
      tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
    });
  }
  ```

  ```bash Shell theme={null}
  # Initial request
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Process this large dataset"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Check stop_reason and handle pause_turn in a loop
  STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.container.id')

  while [ "$STOP_REASON" = "pause_turn" ]; do
    # Continue with same container
    RESPONSE=$(curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
      -H "content-type: application/json" \
      -d "{
        \"model\": \"claude-sonnet-4-5-20250929\",
        \"max_tokens\": 4096,
        \"container\": {
          \"id\": \"$CONTAINER_ID\",
          \"skills\": [{
            \"type\": \"custom\",
            \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
            \"version\": \"latest\"
          }]
        },
        \"messages\": [/* include conversation history */],
        \"tools\": [{
          \"type\": \"code_execution_20250825\",
          \"name\": \"code_execution\"
        }]
      }")

    STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  done
  ```
</CodeGroup>

<Note>
  The response may include a `pause_turn` stop reason, which indicates that the API paused a long-running Skill operation. You can provide the response back as-is in a subsequent request to let Claude continue its turn, or modify the content if you wish to interrupt the conversation and provide additional guidance.
</Note>

### Using Multiple Skills

Combine multiple Skills in a single request to handle complex workflows:

<CodeGroup>
  ```python Python theme={null}
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {
                  "type": "anthropic",
                  "skill_id": "xlsx",
                  "version": "latest"
              },
              {
                  "type": "anthropic",
                  "skill_id": "pptx",
                  "version": "latest"
              },
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest"
              }
          ]
      },
      messages=[{
          "role": "user",
          "content": "Analyze sales data and create a presentation"
      }],
      tools=[{
          "type": "code_execution_20250825",
          "name": "code_execution"
      }]
  )
  ```

  ```typescript TypeScript theme={null}
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {
          type: 'anthropic',
          skill_id: 'xlsx',
          version: 'latest'
        },
        {
          type: 'anthropic',
          skill_id: 'pptx',
          version: 'latest'
        },
        {
          type: 'custom',
          skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          version: 'latest'
        }
      ]
    },
    messages: [{
      role: 'user',
      content: 'Analyze sales data and create a presentation'
    }],
    tools: [{
      type: 'code_execution_20250825',
      name: 'code_execution'
    }]
  });
  ```

  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "xlsx",
            "version": "latest"
          },
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          },
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Analyze sales data and create a presentation"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```
</CodeGroup>

***

## Managing Custom Skills

### Creating a Skill

Upload your custom Skill to make it available in your workspace. You can upload using either a directory path or individual file objects.

<CodeGroup>
  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  # Option 1: Using files_from_dir helper (Python only, recommended)
  from anthropic.lib import files_from_dir

  skill = client.beta.skills.create(
      display_title="Financial Analysis",
      files=files_from_dir("/path/to/financial_analysis_skill"),
      betas=["skills-2025-10-02"]
  )

  # Option 2: Using a zip file
  skill = client.beta.skills.create(
      display_title="Financial Analysis",
      files=[("skill.zip", open("financial_analysis_skill.zip", "rb"))],
      betas=["skills-2025-10-02"]
  )

  # Option 3: Using file tuples (filename, file_content, mime_type)
  skill = client.beta.skills.create(
      display_title="Financial Analysis",
      files=[
          ("financial_skill/SKILL.md", open("financial_skill/SKILL.md", "rb"), "text/markdown"),
          ("financial_skill/analyze.py", open("financial_skill/analyze.py", "rb"), "text/x-python"),
      ],
      betas=["skills-2025-10-02"]
  )

  print(f"Created skill: {skill.id}")
  print(f"Latest version: {skill.latest_version}")
  ```

  ```typescript TypeScript theme={null}
  import Anthropic, { toFile } from '@anthropic-ai/sdk';
  import fs from 'fs';

  const client = new Anthropic();

  // Option 1: Using a zip file
  const skill = await client.beta.skills.create({
    displayTitle: 'Financial Analysis',
    files: [
      await toFile(
        fs.createReadStream('financial_analysis_skill.zip'),
        'skill.zip'
      )
    ],
    betas: ['skills-2025-10-02']
  });

  // Option 2: Using individual file objects
  const skill = await client.beta.skills.create({
    displayTitle: 'Financial Analysis',
    files: [
      await toFile(
        fs.createReadStream('financial_skill/SKILL.md'),
        'financial_skill/SKILL.md',
        { type: 'text/markdown' }
      ),
      await toFile(
        fs.createReadStream('financial_skill/analyze.py'),
        'financial_skill/analyze.py',
        { type: 'text/x-python' }
      ),
    ],
    betas: ['skills-2025-10-02']
  });

  console.log(`Created skill: ${skill.id}`);
  console.log(`Latest version: ${skill.latest_version}`);
  ```

  ```bash Shell theme={null}
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "display_title=Financial Analysis" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
  ```
</CodeGroup>

**Requirements:**

* Must include a SKILL.md file at the top level
* All files must specify a common root directory in their paths
* Total upload size must be under 8MB
* YAML frontmatter requirements:
  * `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
  * `description`: Maximum 1024 characters, non-empty, no XML tags

For complete request/response schemas, see the [Create Skill API reference](/en/api/skills/create-skill).

### Listing Skills

Retrieve all Skills available to your workspace, including both Anthropic pre-built Skills and your custom Skills. Use the `source` parameter to filter by skill type:

<CodeGroup>
  ```python Python theme={null}
  # List all Skills
  skills = client.beta.skills.list(
      betas=["skills-2025-10-02"]
  )

  for skill in skills.data:
      print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

  # List only custom Skills
  custom_skills = client.beta.skills.list(
      source="custom",
      betas=["skills-2025-10-02"]
  )
  ```

  ```typescript TypeScript theme={null}
  // List all Skills
  const skills = await client.beta.skills.list({
    betas: ['skills-2025-10-02']
  });

  for (const skill of skills.data) {
    console.log(`${skill.id}: ${skill.display_title} (source: ${skill.source})`);
  }

  // List only custom Skills
  const customSkills = await client.beta.skills.list({
    source: 'custom',
    betas: ['skills-2025-10-02']
  });
  ```

  ```bash Shell theme={null}
  # List all Skills
  curl "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"

  # List only custom Skills
  curl "https://api.anthropic.com/v1/skills?source=custom" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```
</CodeGroup>

See the [List Skills API reference](/en/api/skills/list-skills) for pagination and filtering options.

### Retrieving a Skill

Get details about a specific Skill:

<CodeGroup>
  ```python Python theme={null}
  skill = client.beta.skills.retrieve(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      betas=["skills-2025-10-02"]
  )

  print(f"Skill: {skill.display_title}")
  print(f"Latest version: {skill.latest_version}")
  print(f"Created: {skill.created_at}")
  ```

  ```typescript TypeScript theme={null}
  const skill = await client.beta.skills.retrieve(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    { betas: ['skills-2025-10-02'] }
  );

  console.log(`Skill: ${skill.display_title}`);
  console.log(`Latest version: ${skill.latest_version}`);
  console.log(`Created: ${skill.created_at}`);
  ```

  ```bash Shell theme={null}
  curl "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```
</CodeGroup>

### Deleting a Skill

To delete a Skill, you must first delete all its versions:

<CodeGroup>
  ```python Python theme={null}
  # Step 1: Delete all versions
  versions = client.beta.skills.versions.list(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      betas=["skills-2025-10-02"]
  )

  for version in versions.data:
      client.beta.skills.versions.delete(
          skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
          version=version.version,
          betas=["skills-2025-10-02"]
      )

  # Step 2: Delete the Skill
  client.beta.skills.delete(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      betas=["skills-2025-10-02"]
  )
  ```

  ```typescript TypeScript theme={null}
  // Step 1: Delete all versions
  const versions = await client.beta.skills.versions.list(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    { betas: ['skills-2025-10-02'] }
  );

  for (const version of versions.data) {
    await client.beta.skills.versions.delete(
      'skill_01AbCdEfGhIjKlMnOpQrStUv',
      version.version,
      { betas: ['skills-2025-10-02'] }
    );
  }

  // Step 2: Delete the Skill
  await client.beta.skills.delete(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    { betas: ['skills-2025-10-02'] }
  );
  ```

  ```bash Shell theme={null}
  # Delete all versions first, then delete the Skill
  curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02"
  ```
</CodeGroup>

Attempting to delete a Skill with existing versions will return a 400 error.

### Versioning

Skills support versioning to manage updates safely:

**Anthropic-Managed Skills**:

* Versions use date format: `20251013`
* New versions released as updates are made
* Specify exact versions for stability

**Custom Skills**:

* Auto-generated epoch timestamps: `1759178010641129`
* Use `"latest"` to always get the most recent version
* Create new versions when updating Skill files

<CodeGroup>
  ```python Python theme={null}
  # Create a new version
  from anthropic.lib import files_from_dir

  new_version = client.beta.skills.versions.create(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      files=files_from_dir("/path/to/updated_skill"),
      betas=["skills-2025-10-02"]
  )

  # Use specific version
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": new_version.version
          }]
      },
      messages=[{"role": "user", "content": "Use updated Skill"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Use latest version
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [{
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "latest"
          }]
      },
      messages=[{"role": "user", "content": "Use latest Skill version"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // Create a new version using a zip file
  const fs = require('fs');

  const newVersion = await client.beta.skills.versions.create(
    'skill_01AbCdEfGhIjKlMnOpQrStUv',
    {
      files: [
        fs.createReadStream('updated_skill.zip')
      ],
      betas: ['skills-2025-10-02']
    }
  );

  // Use specific version
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [{
        type: 'custom',
        skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
        version: newVersion.version
      }]
    },
    messages: [{role: 'user', content: 'Use updated Skill'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Use latest version
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [{
        type: 'custom',
        skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
        version: 'latest'
      }]
    },
    messages: [{role: 'user', content: 'Use latest Skill version'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```

  ```bash Shell theme={null}
  # Create a new version
  NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@updated_skill/SKILL.md;filename=updated_skill/SKILL.md")

  VERSION_NUMBER=$(echo "$NEW_VERSION" | jq -r '.version')

  # Use specific version
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-sonnet-4-5-20250929\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"$VERSION_NUMBER\"
        }]
      },
      \"messages\": [{\"role\": \"user\", \"content\": \"Use updated Skill\"}],
      \"tools\": [{\"type\": \"code_execution_20250825\", \"name\": \"code_execution\"}]
    }"

  # Use latest version
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }]
      },
      "messages": [{"role": "user", "content": "Use latest Skill version"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```
</CodeGroup>

See the [Create Skill Version API reference](/en/api/skills/create-skill-version) for complete details.

***

## How Skills Are Loaded

When you specify Skills in a container:

1. **Metadata Discovery**: Claude sees metadata for each Skill (name, description) in the system prompt
2. **File Loading**: Skill files are copied into the container at `/skills/{directory}/`
3. **Automatic Use**: Claude automatically loads and uses Skills when relevant to your request
4. **Composition**: Multiple Skills compose together for complex workflows

The progressive disclosure architecture ensures efficient context usage—Claude only loads full Skill instructions when needed.

***

## Use Cases

### Organizational Skills

**Brand & Communications**

* Apply company-specific formatting (colors, fonts, layouts) to documents
* Generate communications following organizational templates
* Ensure consistent brand guidelines across all outputs

**Project Management**

* Structure notes with company-specific formats (OKRs, decision logs)
* Generate tasks following team conventions
* Create standardized meeting recaps and status updates

**Business Operations**

* Create company-standard reports, proposals, and analyses
* Execute company-specific analytical procedures
* Generate financial models following organizational templates

### Personal Skills

**Content Creation**

* Custom document templates
* Specialized formatting and styling
* Domain-specific content generation

**Data Analysis**

* Custom data processing pipelines
* Specialized visualization templates
* Industry-specific analytical methods

**Development & Automation**

* Code generation templates
* Testing frameworks
* Deployment workflows

### Example: Financial Modeling

Combine Excel and custom DCF analysis Skills:

<CodeGroup>
  ```python Python theme={null}
  # Create custom DCF analysis Skill
  from anthropic.lib import files_from_dir

  dcf_skill = client.beta.skills.create(
      display_title="DCF Analysis",
      files=files_from_dir("/path/to/dcf_skill"),
      betas=["skills-2025-10-02"]
  )

  # Use with Excel to create financial model
  response = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "custom", "skill_id": dcf_skill.id, "version": "latest"}
          ]
      },
      messages=[{
          "role": "user",
          "content": "Build a DCF valuation model for a SaaS company with the attached financials"
      }],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // Create custom DCF analysis Skill
  import { toFile } from '@anthropic-ai/sdk';
  import fs from 'fs';

  const dcfSkill = await client.beta.skills.create({
    displayTitle: 'DCF Analysis',
    files: [
      await toFile(fs.createReadStream('dcf_skill.zip'), 'skill.zip')
    ],
    betas: ['skills-2025-10-02']
  });

  // Use with Excel to create financial model
  const response = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'},
        {type: 'custom', skill_id: dcfSkill.id, version: 'latest'}
      ]
    },
    messages: [{
      role: 'user',
      content: 'Build a DCF valuation model for a SaaS company with the attached financials'
    }],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```

  ```bash Shell theme={null}
  # Create custom DCF analysis Skill
  DCF_SKILL=$(curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "display_title=DCF Analysis" \
    -F "files[]=@dcf_skill/SKILL.md;filename=dcf_skill/SKILL.md")

  DCF_SKILL_ID=$(echo "$DCF_SKILL" | jq -r '.id')

  # Use with Excel to create financial model
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-sonnet-4-5-20250929\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [
          {
            \"type\": \"anthropic\",
            \"skill_id\": \"xlsx\",
            \"version\": \"latest\"
          },
          {
            \"type\": \"custom\",
            \"skill_id\": \"$DCF_SKILL_ID\",
            \"version\": \"latest\"
          }
        ]
      },
      \"messages\": [{
        \"role\": \"user\",
        \"content\": \"Build a DCF valuation model for a SaaS company with the attached financials\"
      }],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }"
  ```
</CodeGroup>

***

## Limits and Constraints

### Request Limits

* **Maximum Skills per request**: 8
* **Maximum Skill upload size**: 8MB (all files combined)
* **YAML frontmatter requirements**:
  * `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words
  * `description`: Maximum 1024 characters, non-empty, no XML tags

### Environment Constraints

Skills run in the code execution container with these limitations:

* **No network access** - Cannot make external API calls
* **No runtime package installation** - Only pre-installed packages available
* **Isolated environment** - Each request gets a fresh container

See the [code execution tool documentation](/en/docs/agents-and-tools/tool-use/code-execution-tool) for available packages.

***

## Best Practices

### When to Use Multiple Skills

Combine Skills when tasks involve multiple document types or domains:

**Good use cases:**

* Data analysis (Excel) + presentation creation (PowerPoint)
* Report generation (Word) + export to PDF
* Custom domain logic + document generation

**Avoid:**

* Including unused Skills (impacts performance)

### Version Management Strategy

**For production:**

```python  theme={null}
# Pin to specific versions for stability
container={
    "skills": [{
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "1759178010641129"  # Specific version
    }]
}
```

**For development:**

```python  theme={null}
# Use latest for active development
container={
    "skills": [{
        "type": "custom",
        "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
        "version": "latest"  # Always get newest
    }]
}
```

### Prompt Caching Considerations

When using prompt caching, note that changing the Skills list in your container will break the cache:

<CodeGroup>
  ```python Python theme={null}
  # First request creates cache
  response1 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
          ]
      },
      messages=[{"role": "user", "content": "Analyze sales data"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )

  # Adding/removing Skills breaks cache
  response2 = client.beta.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=4096,
      betas=["code-execution-2025-08-25", "skills-2025-10-02", "prompt-caching-2024-07-31"],
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "anthropic", "skill_id": "pptx", "version": "latest"}  # Cache miss
          ]
      },
      messages=[{"role": "user", "content": "Create a presentation"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
  )
  ```

  ```typescript TypeScript theme={null}
  // First request creates cache
  const response1 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02', 'prompt-caching-2024-07-31'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'}
      ]
    },
    messages: [{role: 'user', content: 'Analyze sales data'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });

  // Adding/removing Skills breaks cache
  const response2 = await client.beta.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 4096,
    betas: ['code-execution-2025-08-25', 'skills-2025-10-02', 'prompt-caching-2024-07-31'],
    container: {
      skills: [
        {type: 'anthropic', skill_id: 'xlsx', version: 'latest'},
        {type: 'anthropic', skill_id: 'pptx', version: 'latest'}  // Cache miss
      ]
    },
    messages: [{role: 'user', content: 'Create a presentation'}],
    tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
  });
  ```

  ```bash Shell theme={null}
  # First request creates cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Analyze sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'

  # Adding/removing Skills breaks cache
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,prompt-caching-2024-07-31" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-5-20250929",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
          {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Create a presentation"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```
</CodeGroup>

For best caching performance, keep your Skills list consistent across requests.

### Error Handling

Handle Skill-related errors gracefully:

<CodeGroup>
  ```python Python theme={null}
  try:
      response = client.beta.messages.create(
          model="claude-sonnet-4-5-20250929",
          max_tokens=4096,
          betas=["code-execution-2025-08-25", "skills-2025-10-02"],
          container={
              "skills": [
                  {"type": "custom", "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv", "version": "latest"}
              ]
          },
          messages=[{"role": "user", "content": "Process data"}],
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
      )
  except anthropic.BadRequestError as e:
      if "skill" in str(e):
          print(f"Skill error: {e}")
          # Handle skill-specific errors
      else:
          raise
  ```

  ```typescript TypeScript theme={null}
  try {
    const response = await client.beta.messages.create({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 4096,
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: {
        skills: [
          {type: 'custom', skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv', version: 'latest'}
        ]
      },
      messages: [{role: 'user', content: 'Process data'}],
      tools: [{type: 'code_execution_20250825', name: 'code_execution'}]
    });
  } catch (error) {
    if (error instanceof Anthropic.BadRequestError && error.message.includes('skill')) {
      console.error(`Skill error: ${error.message}`);
      // Handle skill-specific errors
    } else {
      throw error;
    }
  }
  ```
</CodeGroup>

***

## Next Steps

<CardGroup cols={2}>
  <Card title="API Reference" icon="book" href="/en/api/skills/create-skill">
    Complete API reference with all endpoints
  </Card>

  <Card title="Authoring Guide" icon="pen" href="/en/docs/agents-and-tools/agent-skills/best-practices">
    Best practices for writing effective Skills
  </Card>

  <Card title="Code Execution Tool" icon="terminal" href="/en/docs/agents-and-tools/tool-use/code-execution-tool">
    Learn about the code execution environment
  </Card>
</CardGroup>
# Get Skill

## OpenAPI

````yaml get /v1/skills/{skill_id}
paths:
  path: /v1/skills/{skill_id}
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
      query: {}
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.beta.skills.retrieve(
              "skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
          )
      - lang: javascript
        source: >-
          import Anthropic from '@anthropic-ai/sdk';


          const anthropic = new Anthropic();


          await anthropic.beta.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv",
          {{
            betas: ["skills-2025-10-02"],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              created_at:
                allOf:
                  - type: string
                    title: Created At
                    description: ISO 8601 timestamp of when the skill was created.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
              display_title:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Display Title
                    description: >-
                      Display title for the skill.


                      This is a human-readable label that is not included in the
                      prompt sent to the model.
                    examples:
                      - My Custom Skill
              id:
                allOf:
                  - type: string
                    title: Id
                    description: |-
                      Unique identifier for the skill.

                      The format and length of IDs may change over time.
                    examples:
                      - skill_01JAbcdefghijklmnopqrstuvw
              latest_version:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Latest Version
                    description: >-
                      The latest version identifier for the skill.


                      This represents the most recent version of the skill that
                      has been created.
                    examples:
                      - '1759178010641129'
              source:
                allOf:
                  - type: string
                    title: Source
                    description: |-
                      Source of the skill.

                      This may be one of the following values:
                      * `"custom"`: the skill was created by a user
                      * `"anthropic"`: the skill was created by Anthropic
                    examples:
                      - custom
              type:
                allOf:
                  - type: string
                    title: Type
                    description: |-
                      Object type.

                      For Skills, this is always `"skill"`.
                    default: skill
              updated_at:
                allOf:
                  - type: string
                    title: Updated At
                    description: ISO 8601 timestamp of when the skill was last updated.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
            title: GetSkillResponse
            refIdentifier: '#/components/schemas/GetSkillResponse'
            requiredProperties:
              - created_at
              - display_title
              - id
              - latest_version
              - source
              - type
              - updated_at
        examples:
          example:
            value:
              created_at: '2024-10-30T23:58:27.427722Z'
              display_title: My Custom Skill
              id: skill_01JAbcdefghijklmnopqrstuvw
              latest_version: '1759178010641129'
              source: custom
              type: skill
              updated_at: '2024-10-30T23:58:27.427722Z'
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object

````
# Delete Skill

## OpenAPI

````yaml delete /v1/skills/{skill_id}
paths:
  path: /v1/skills/{skill_id}
  method: delete
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
      query: {}
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl -X DELETE
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.beta.skills.delete(
              "skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
          )
      - lang: javascript
        source: >-
          import Anthropic from '@anthropic-ai/sdk';


          const anthropic = new Anthropic();


          await anthropic.beta.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv",
          {{
            betas: ["skills-2025-10-02"],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              id:
                allOf:
                  - type: string
                    title: Id
                    description: |-
                      Unique identifier for the skill.

                      The format and length of IDs may change over time.
                    examples:
                      - skill_01JAbcdefghijklmnopqrstuvw
              type:
                allOf:
                  - type: string
                    title: Type
                    description: |-
                      Deleted object type.

                      For Skills, this is always `"skill_deleted"`.
                    default: skill_deleted
            title: DeleteSkillResponse
            refIdentifier: '#/components/schemas/DeleteSkillResponse'
            requiredProperties:
              - id
              - type
        examples:
          example:
            value:
              id: skill_01JAbcdefghijklmnopqrstuvw
              type: skill_deleted
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object

````

# Create Skill Version

## OpenAPI

````yaml post /v1/skills/{skill_id}/versions
paths:
  path: /v1/skills/{skill_id}/versions
  method: post
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
      query: {}
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body:
      multipart/form-data:
        schemaArray:
          - type: object
            properties:
              files:
                allOf:
                  - anyOf:
                      - items:
                          type: string
                          format: binary
                        type: array
                      - type: 'null'
                    title: Files
                    description: >-
                      Files to upload for the skill.


                      All files must be in the same top-level directory and must
                      include a SKILL.md file at the root of that directory.
            title: Body_create_skill_version_v1_skills__skill_id__versions_post
            refIdentifier: >-
              #/components/schemas/Body_create_skill_version_v1_skills__skill_id__versions_post
        examples:
          example:
            value:
              files:
                - null
    codeSamples:
      - lang: bash
        source: >-
          curl -X POST
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions"
          \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02" \
               -F "files[]=@excel-skill/SKILL.md;filename=excel-skill/SKILL.md" \
               -F "files[]=@excel-skill/process_excel.py;filename=excel-skill/process_excel.py"
      - lang: python
        source: |-
          import anthropic
          from anthropic.lib import files_from_dir

          client = anthropic.Anthropic()

          # Option 1: Using files_from_dir helper
          client.beta.skills.versions.create(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
              files=files_from_dir("excel-skill"),
          )

          # Option 2: Using a zip file
          client.beta.skills.versions.create(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
              files=[open("excel-skill.zip", "rb")],
          )

          # Option 3: Using file tuples (filename, file_content, mime_type)
          client.beta.skills.versions.create(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
              files=[
                  ("excel-skill/SKILL.md", open("excel-skill/SKILL.md", "rb"), "text/markdown"),
                  ("excel-skill/process_excel.py", open("excel-skill/process_excel.py", "rb"), "text/x-python"),
              ],
          )
      - lang: javascript
        source: >-
          import Anthropic, {{ toFile }} from '@anthropic-ai/sdk';

          import fs from 'fs';


          const anthropic = new Anthropic();


          // Option 1: Using a zip file

          await
          anthropic.beta.skills.versions.create('skill_01AbCdEfGhIjKlMnOpQrStUv',
          {{
            betas: ["skills-2025-10-02"],
            files: [fs.createReadStream('excel-skill.zip')],
          }});


          // Option 2: Using individual files

          await
          anthropic.beta.skills.versions.create('skill_01AbCdEfGhIjKlMnOpQrStUv',
          {{
            betas: ["skills-2025-10-02"],
            files: [
              await toFile(fs.createReadStream('excel-skill/SKILL.md'), 'excel-skill/SKILL.md'),
              await toFile(fs.createReadStream('excel-skill/process_excel.py'), 'excel-skill/process_excel.py'),
            ],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              created_at:
                allOf:
                  - type: string
                    title: Created At
                    description: ISO 8601 timestamp of when the skill version was created.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
              description:
                allOf:
                  - type: string
                    title: Description
                    description: >-
                      Description of the skill version.


                      This is extracted from the SKILL.md file in the skill
                      upload.
                    examples:
                      - A custom skill for doing something useful
              directory:
                allOf:
                  - type: string
                    title: Directory
                    description: >-
                      Directory name of the skill version.


                      This is the top-level directory name that was extracted
                      from the uploaded files.
                    examples:
                      - my-skill
              id:
                allOf:
                  - type: string
                    title: Id
                    description: |-
                      Unique identifier for the skill version.

                      The format and length of IDs may change over time.
                    examples:
                      - skillver_01JAbcdefghijklmnopqrstuvw
              name:
                allOf:
                  - type: string
                    title: Name
                    description: >-
                      Human-readable name of the skill version.


                      This is extracted from the SKILL.md file in the skill
                      upload.
                    examples:
                      - my-skill
              skill_id:
                allOf:
                  - type: string
                    title: Skill Id
                    description: Identifier for the skill that this version belongs to.
                    examples:
                      - skill_01JAbcdefghijklmnopqrstuvw
              type:
                allOf:
                  - type: string
                    title: Type
                    description: |-
                      Object type.

                      For Skill Versions, this is always `"skill_version"`.
                    default: skill_version
              version:
                allOf:
                  - type: string
                    title: Version
                    description: >-
                      Version identifier for the skill.


                      Each version is identified by a Unix epoch timestamp
                      (e.g., "1759178010641129").
                    examples:
                      - '1759178010641129'
            title: CreateSkillVersionResponse
            refIdentifier: '#/components/schemas/CreateSkillVersionResponse'
            requiredProperties:
              - created_at
              - description
              - directory
              - id
              - name
              - skill_id
              - type
              - version
        examples:
          example:
            value:
              created_at: '2024-10-30T23:58:27.427722Z'
              description: A custom skill for doing something useful
              directory: my-skill
              id: skillver_01JAbcdefghijklmnopqrstuvw
              name: my-skill
              skill_id: skill_01JAbcdefghijklmnopqrstuvw
              type: skill_version
              version: '1759178010641129'
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object

````

# List Skill Versions

## OpenAPI

````yaml get /v1/skills/{skill_id}/versions
paths:
  path: /v1/skills/{skill_id}/versions
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
      query:
        page:
          schema:
            - type: string
              required: false
              title: Page
              description: >-
                Optionally set to the `next_page` token from the previous
                response.
            - type: 'null'
              required: false
              title: Page
              description: >-
                Optionally set to the `next_page` token from the previous
                response.
        limit:
          schema:
            - type: integer
              required: false
              title: Limit
              description: |-
                Number of items to return per page.

                Defaults to `20`. Ranges from `1` to `1000`.
            - type: 'null'
              required: false
              title: Limit
              description: |-
                Number of items to return per page.

                Defaults to `20`. Ranges from `1` to `1000`.
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions"
          \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.beta.skills.versions.list(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
          )
      - lang: javascript
        source: >-
          import Anthropic from '@anthropic-ai/sdk';


          const anthropic = new Anthropic();


          await
          anthropic.beta.skills.versions.list('skill_01AbCdEfGhIjKlMnOpQrStUv',
          {{
            betas: ["skills-2025-10-02"],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              data:
                allOf:
                  - items:
                      $ref: '#/components/schemas/SkillVersion'
                    type: array
                    title: Data
                    description: List of skill versions.
              has_more:
                allOf:
                  - type: boolean
                    title: Has More
                    description: >-
                      Indicates if there are more results in the requested page
                      direction.
              next_page:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Next Page
                    description: >-
                      Token to provide in as `page` in the subsequent request to
                      retrieve the next page of data.
                    examples:
                      - page_MjAyNS0wNS0xNFQwMDowMDowMFo=
                      - null
            title: ListSkillVersionsResponse
            refIdentifier: '#/components/schemas/ListSkillVersionsResponse'
            requiredProperties:
              - data
              - has_more
              - next_page
        examples:
          example:
            value:
              data:
                - created_at: '2024-10-30T23:58:27.427722Z'
                  description: A custom skill for doing something useful
                  directory: my-skill
                  id: skillver_01JAbcdefghijklmnopqrstuvw
                  name: my-skill
                  skill_id: skill_01JAbcdefghijklmnopqrstuvw
                  type: skill_version
                  version: '1759178010641129'
              has_more: true
              next_page: page_MjAyNS0wNS0xNFQwMDowMDowMFo=
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object
    SkillVersion:
      properties:
        created_at:
          type: string
          title: Created At
          description: ISO 8601 timestamp of when the skill version was created.
          examples:
            - '2024-10-30T23:58:27.427722Z'
        description:
          type: string
          title: Description
          description: |-
            Description of the skill version.

            This is extracted from the SKILL.md file in the skill upload.
          examples:
            - A custom skill for doing something useful
        directory:
          type: string
          title: Directory
          description: >-
            Directory name of the skill version.


            This is the top-level directory name that was extracted from the
            uploaded files.
          examples:
            - my-skill
        id:
          type: string
          title: Id
          description: |-
            Unique identifier for the skill version.

            The format and length of IDs may change over time.
          examples:
            - skillver_01JAbcdefghijklmnopqrstuvw
        name:
          type: string
          title: Name
          description: |-
            Human-readable name of the skill version.

            This is extracted from the SKILL.md file in the skill upload.
          examples:
            - my-skill
        skill_id:
          type: string
          title: Skill Id
          description: Identifier for the skill that this version belongs to.
          examples:
            - skill_01JAbcdefghijklmnopqrstuvw
        type:
          type: string
          title: Type
          description: |-
            Object type.

            For Skill Versions, this is always `"skill_version"`.
          default: skill_version
        version:
          type: string
          title: Version
          description: >-
            Version identifier for the skill.


            Each version is identified by a Unix epoch timestamp (e.g.,
            "1759178010641129").
          examples:
            - '1759178010641129'
      type: object
      required:
        - created_at
        - description
        - directory
        - id
        - name
        - skill_id
        - type
        - version
      title: SkillVersion

````

# Get Skill Version

## OpenAPI

````yaml get /v1/skills/{skill_id}/versions/{version}
paths:
  path: /v1/skills/{skill_id}/versions/{version}
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
        version:
          schema:
            - type: string
              required: true
              title: Version
              description: >-
                Version identifier for the skill.


                Each version is identified by a Unix epoch timestamp (e.g.,
                "1759178010641129").
      query: {}
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions/1759178010641129"
          \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.beta.skills.versions.retrieve(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              version="1759178010641129",
              betas=["skills-2025-10-02"],
          )
      - lang: javascript
        source: |-
          import Anthropic from '@anthropic-ai/sdk';

          const anthropic = new Anthropic();

          await anthropic.beta.skills.versions.retrieve('1759178010641129', {{
            skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
            betas: ["skills-2025-10-02"],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              created_at:
                allOf:
                  - type: string
                    title: Created At
                    description: ISO 8601 timestamp of when the skill version was created.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
              description:
                allOf:
                  - type: string
                    title: Description
                    description: >-
                      Description of the skill version.


                      This is extracted from the SKILL.md file in the skill
                      upload.
                    examples:
                      - A custom skill for doing something useful
              directory:
                allOf:
                  - type: string
                    title: Directory
                    description: >-
                      Directory name of the skill version.


                      This is the top-level directory name that was extracted
                      from the uploaded files.
                    examples:
                      - my-skill
              id:
                allOf:
                  - type: string
                    title: Id
                    description: |-
                      Unique identifier for the skill version.

                      The format and length of IDs may change over time.
                    examples:
                      - skillver_01JAbcdefghijklmnopqrstuvw
              name:
                allOf:
                  - type: string
                    title: Name
                    description: >-
                      Human-readable name of the skill version.


                      This is extracted from the SKILL.md file in the skill
                      upload.
                    examples:
                      - my-skill
              skill_id:
                allOf:
                  - type: string
                    title: Skill Id
                    description: Identifier for the skill that this version belongs to.
                    examples:
                      - skill_01JAbcdefghijklmnopqrstuvw
              type:
                allOf:
                  - type: string
                    title: Type
                    description: |-
                      Object type.

                      For Skill Versions, this is always `"skill_version"`.
                    default: skill_version
              version:
                allOf:
                  - type: string
                    title: Version
                    description: >-
                      Version identifier for the skill.


                      Each version is identified by a Unix epoch timestamp
                      (e.g., "1759178010641129").
                    examples:
                      - '1759178010641129'
            title: GetSkillVersionResponse
            refIdentifier: '#/components/schemas/GetSkillVersionResponse'
            requiredProperties:
              - created_at
              - description
              - directory
              - id
              - name
              - skill_id
              - type
              - version
        examples:
          example:
            value:
              created_at: '2024-10-30T23:58:27.427722Z'
              description: A custom skill for doing something useful
              directory: my-skill
              id: skillver_01JAbcdefghijklmnopqrstuvw
              name: my-skill
              skill_id: skill_01JAbcdefghijklmnopqrstuvw
              type: skill_version
              version: '1759178010641129'
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object

````

# Delete Skill Version

## OpenAPI

````yaml delete /v1/skills/{skill_id}/versions/{version}
paths:
  path: /v1/skills/{skill_id}/versions/{version}
  method: delete
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
        version:
          schema:
            - type: string
              required: true
              title: Version
              description: >-
                Version identifier for the skill.


                Each version is identified by a Unix epoch timestamp (e.g.,
                "1759178010641129").
      query: {}
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl -X DELETE
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions/1759178010641129"
          \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.beta.skills.versions.delete(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              version="1759178010641129",
              betas=["skills-2025-10-02"],
          )
      - lang: javascript
        source: |-
          import Anthropic from '@anthropic-ai/sdk';

          const anthropic = new Anthropic();

          await anthropic.beta.skills.versions.delete('1759178010641129', {{
            skill_id: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
            betas: ["skills-2025-10-02"],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              id:
                allOf:
                  - type: string
                    title: Id
                    description: >-
                      Version identifier for the skill.


                      Each version is identified by a Unix epoch timestamp
                      (e.g., "1759178010641129").
                    examples:
                      - '1759178010641129'
              type:
                allOf:
                  - type: string
                    title: Type
                    description: >-
                      Deleted object type.


                      For Skill Versions, this is always
                      `"skill_version_deleted"`.
                    default: skill_version_deleted
            title: DeleteSkillVersionResponse
            refIdentifier: '#/components/schemas/DeleteSkillVersionResponse'
            requiredProperties:
              - id
              - type
        examples:
          example:
            value:
              id: '1759178010641129'
              type: skill_version_deleted
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object

````