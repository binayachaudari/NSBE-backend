# NSBE Hack

### Chat Endpoint

METHOD: `POST`

URL: `https://nsbe-backend.onrender.com/chat/`

CONTENT-TYPE: `application/json`

PAYLOAD:

```json
{
  "message": "what are the documents required for the international stuents to rent a place in toronto"
}
```

SAMPLE RESPONSE

```json
{
  "text": "Landlords in Toronto must use a standard lease template and the lease must contain the landlord's legal name and address. Within 21 days of the tenancy beginning, the landlord must provide a copy of the signed tenancy agreement to the tenant.\n\nPotential tenants need to be aware that landlords are prohibited from discriminating against them based on characteristics such as religion, ethnic background, sexual orientation, whether they have a disability, or their age. However, the specific documents needed to rent a place in Toronto are not clear from my sources. The process might vary depending on the landlord and it is best to check with the relevant authorities beforehand.",
  "generation_id": "542f1f00-8334-4a33-a174-2ddb6b508bb7",
  "citations": [
    {
      "start": 0,
      "end": 55,
      "text": "Landlords in Toronto must use a standard lease template",
      "document_ids": ["doc_4"]
    },
    {
      "start": 70,
      "end": 121,
      "text": "must contain the landlord's legal name and address.",
      "document_ids": ["doc_4"]
    },
    {
      "start": 129,
      "end": 242,
      "text": "21 days of the tenancy beginning, the landlord must provide a copy of the signed tenancy agreement to the tenant.",
      "document_ids": ["doc_4"]
    },
    {
      "start": 284,
      "end": 341,
      "text": "landlords are prohibited from discriminating against them",
      "document_ids": ["doc_2"]
    },
    {
      "start": 375,
      "end": 469,
      "text": "religion, ethnic background, sexual orientation, whether they have a disability, or their age.",
      "document_ids": ["doc_2"]
    }
  ],
  "documents": [
    {
      "id": "doc_4",
      "text": "Landlords\n\nMost landlords must use the standard lease template.\n\nThe lease must contain the legal name and address of the landlord.\n\nThe landlord must provide a copy of a signed tenancy agreement to the tenant within 21 days of the tenancy beginning.",
      "title": "Rights & Responsibilities for Landlords & Tenants",
      "url": "https://www.toronto.ca/community-people/housing-shelter/rental-housing-tenant-information/rights-responsibilities-for-landlords-tenants/"
    },
    {
      "id": "doc_2",
      "text": "your religion or ethnic background\n\nyour sexual orientation\n\nif you get welfare or other public assistance\n\nif you have a disability\n\nyour age (even if you are 16 or 17 as long as you are living away from your parents)\n\nif you are a Canadian citizen\n\nA landlord must not discriminate against potential tenants.",
      "title": "Rights & Responsibilities for Landlords & Tenants",
      "url": "https://www.toronto.ca/community-people/housing-shelter/rental-housing-tenant-information/rights-responsibilities-for-landlords-tenants/"
    }
  ],
  "is_search_required": null,
  "search_results": null,
  "finish_reason": "COMPLETE",
  "chat_history": null,
  "message": "what are the documents required for the international stuents to rent a place in toronto",
  "response_id": "8b364773-e425-4768-b235-e8b50acc67dc",
  "token_count": {
    "prompt_tokens": 1122,
    "response_tokens": 125,
    "total_tokens": 1247,
    "billed_tokens": 172
  },
  "conversation_id": "cc984af5-2a9f-41ae-b751-783c03fc5331"
}
```
