[![](https://img.shields.io/badge/kariya_1.0.0-build-passing)](https://github.com/gongahkia/kariya/releases/tag/1.0.0)

# `Kariya` 🌻

Tiny Web App that analyses and [scores](#screenshot) the legibility of your handwriting.

`Kariya` is trained on the [ImageNet](https://www.image-net.org/) database.

<div align="center">
  <img src="./asset/reference/1.png" width="80%">
</div>

## Stack

* Frontend *(Vue.js, Tailwind CSS, Netlify)*
* Backend *(Flask)*
* DB *(Firebase Realtime Database)*
* Training and Validation Corpus *(ImageNet)*

## Screenshot

<div style="display: flex; justify-content: space-between;">
  <img src="./asset/reference/cooked.png" width="48%">
  <img src="./asset/reference/not_cooked.png" width="48%">
</div>

## Usage

```console
$ git clone https://github.com/gongahkia/kariya
$ cd kariya/kariya-app
$ npm install
$ cd ../backend
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip install -r requirements.txt
$ cd ..
$ python3 main.py
```

## Architecture

### Overview

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Vue.js Frontend
    participant Backend as Flask Backend
    participant ImageNet as ImageNet Service
    participant DB as Firebase Realtime Database
    participant Social as Instagram, Facebook, LinkedIn API

    User->>Frontend: Writes on canvas
    Frontend->>Frontend: Captures handwriting strokes
    
    User->>Frontend: Clicks "Analyze" button
    Frontend->>Backend: POST /api/analyze with image data
    
    Backend->>Backend: Preprocesses image
    Backend->>ImageNet: Send processed image for classification
    ImageNet->>Backend: Return classification results
    
    Backend->>Backend: Calculate legibility score
    Backend->>Backend: Calculate consistency score
    Backend->>Backend: Determine if handwriting is "cooked"
    
    Backend->>DB: Store analysis results
    DB->>Backend: Confirm storage
    
    Backend->>Frontend: Return analysis results
    Frontend->>Frontend: Display scores and verdict
    
    User->>Frontend: Clicks "Share" button
    Frontend->>Social: Request sharing to selected platform
    Social->>User: Open sharing dialog
    
    User->>Frontend: Clicks "Clear" button
    Frontend->>Frontend: Reset canvas
    
    alt User wants to save results
        User->>Frontend: Clicks "Save" button
        Frontend->>Backend: POST /api/save with user ID and results
        Backend->>DB: Store user results
        DB->>Backend: Confirm storage
        Backend->>Frontend: Return success status
    end
    
    loop Improvement cycle
        Backend->>DB: Fetch historical data
        DB->>Backend: Return historical data
        Backend->>Backend: Refine scoring algorithm
    end
```

### Database

```json
{
  "users": {
    "$userId": {
      "name": "String",
      "email": "String",
      "profile_picture": "String",
      "analyses": {
        "$analysisId": {
          "timestamp": "Timestamp",
          "imageUrl": "String",
          "legibilityScore": "Number",
          "consistencyScore": "Number",
          "totalScore": "Number",
          "isCooked": "Boolean",
          "classification": "String",
          "confidence": "Number",
          "characterRecognition": {
            "$character": "Number"
          },
          "feedback": "String"
        }
      }
    }
  },
  "analyses": {
    "$analysisId": {
      "userId": "String",
      "timestamp": "Timestamp",
      "imageUrl": "String",
      "legibilityScore": "Number",
      "consistencyScore": "Number",
      "totalScore": "Number",
      "isCooked": "Boolean",
      "classification": "String",
      "strokes": [
        {
          "points": [
            {
              "x": "Number",
              "y": "Number",
              "time": "Number"
            }
          ],
          "pressure": "Number"
        }
      ],
      "trainingContribution": "Boolean"
    }
  },
  "modelVersions": {
    "$versionId": {
      "releaseDate": "Timestamp",
      "accuracy": "Number",
      "precision": "Number",
      "recall": "Number",
      "f1Score": "Number",
      "trainingSamples": "Number",
      "active": "Boolean"
    }
  }
}
```

### Backend

```mermaid
flowchart TD
    A[User's Handwriting Sample] --> B[Image Preprocessing]
    B --> C[Feature Extraction]
    C --> D[Feature Vector Matrix]
    
    E[(ImageNet Corpus)] --> F[Character Recognition Models]
    F --> G[Pre-trained Model Weights]
    
    D --> H@{ shape: docs, label: "Training Dataset"}
    G --> H
    
    H --> I@{ shape: rounded, label: "Supervised ML training epoch" }
    I --> J[Legibility Classifier Training]
    
    K[(Expert-Labeled Legibility Data)] --> H
    
    J --> L[Trained Handwriting Legibility Model]
    
    M{New Handwriting Sample} --> N[Process New Sample]
    N --> O[Extract Spatial Features]
    O --> P[Legibility Analysis]
    L --> P
    P --> Q[Legibility & Recognizability Score]
    
    D --> R
    G --> R
    K --> R
    R@{ shape: docs, label: "Validation Dataset" } --> S[Model Validation]
    L --> S
    S --> T[Performance Metrics]
    T --> U[Model Refinement]
    U --> I
```

## Reference

The name `Kariya` is in reference to [Kariya Kagetoki](https://champloo.fandom.com/wiki/Kariya_Kagetoki) *(better known as the "Hand of God")*, an elite samurai working for the Shogunate. He first makes an appearance in the episode, [Evanescent Encounter Part 1](https://champloo.fandom.com/wiki/Evanescent_Encounter_(Part_1)) of the anime [Samurai Champloo](https://champloo.fandom.com/wiki/Samurai_Champloo_Wiki).

![](./asset/logo/kariya.webp)