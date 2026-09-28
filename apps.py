from graph import research_graph


question = "What is LangGraph?"

result = research_graph.invoke({
    "question": question,
    "search_results": [],
    "scraped_content": [],
    "extracted_information": ""
})

# for page in result["scraped_content"]:
#     print("\nURL:", page["url"])
#     print("CONTENT:", page["content"][:1000])

from graph import research_graph


question = "What is LangGraph?"

result = research_graph.invoke({
    "question": question,
    "search_results": [],
    "scraped_content": [],
    "extracted_information": "",
    "is_valid": False,
    "validation_feedback": "",
    "attempts": 0
})

print("\n===== EXTRACTED INFORMATION =====\n")
print(result["extracted_information"])

print("\n===== VALIDATION =====\n")
print("Valid:", result["is_valid"])
print("Feedback:", result["validation_feedback"])