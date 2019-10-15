"""Mongo aggregation pipelines."""

organizations_pipeline = [
    {"$match": {
        "affiliations.id": {"$exists": True}
    }},
    {"$project": {
        "affiliations": 1,
        "id": 1,
        "_id": 0,
        "keywords_fr": 1,
        "keywords_en": 1,
        "title": 1,
    }},
    {"$addFields": {
        "affiliations": "$affiliations.id",
        "keywords": {
            "$setUnion": [{"$ifNull": ["$keywords_fr", []]}, {"$ifNull": ["$keywords_en", []]}]
        },
    }},
    {"$project": {"keywords_fr": 0, "keywords_en": 0}},
    {"$out": "organizations"}
]


authors_pipeline = [
    {"$addFields": {
        "authorsList": {
            "$reduce": {
                "input": "$authors.id",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        {"$cond": {
                             "if": { "$isArray": "$$this" },
                             "then": "$$this",
                             "else": ["$$this"]
                        }}
                    ]
                }
            }
        }
    }},
    {"$unwind": "$authorsList"},
    {"$group":{
        "_id": "$_id",
        "doc":{"$first":"$$ROOT"},
        "coAuthors": {
            "$addToSet": "$authorsList"
        }
    }},
    {"$addFields": {
        "doc.coAuthors": "$coAuthors"
    }},
    {"$replaceRoot":{"newRoot":"$doc"}},
    {"$unwind": "$authors"},
    {"$match": {"authors.id": {"$exists": True}}},
    {"$unwind": {"path": "$authors.affiliations", "preserveNullAndEmptyArrays": True}},
    {"$unwind": {"path": "$thematics", "preserveNullAndEmptyArrays": True}},
    {"$unwind": {"path": "$keywords_fr", "preserveNullAndEmptyArrays": True}},
    {"$unwind": {"path": "$keywords_en", "preserveNullAndEmptyArrays": True}},
    {"$unwind": {"path": "$funding_info", "preserveNullAndEmptyArrays": True}},
    {
        "$group": {
            "_id": "$authors.id",
            "coAuthors": {
                "$addToSet": "$coAuthors"
            },
            "publications": {
                "$addToSet": {
                    "publication": "$id",
                    "role": "$authors.role"
                }
            },
            "affiliations": {
                "$addToSet": {
                    "affiliation": "$authors.affiliations.id",
                    "source": "$id",
                    "year": {
                        "$ifNull": [
                            {"$year": "$publication_date"},
                            {"$year": "$thesis_informations.defense_date"}
                        ]
                    }
                }
            },
            "thematics": {
                "$addToSet": {
                    "label": {
                        "en": "$thematics.en_label",
                        "fr": "$thematics.fr_label"
                    },
                    "type": "$thematics.reference",
                    "code": "$thematics.code",
                }
            },
            "keywords_fr": {"$addToSet": "$keywords_fr"},
            "keywords_en": {"$addToSet": "$keywords_en"},
            "fundings": {"$addToSet": "$funding_info.funding_ref"}
        }
    },
    {"$addFields": {
        "coAuthors": {
            "$reduce": {
                "input": "$coAuthors",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        {"$cond": {
                             "if": { "$isArray": "$$this" },
                             "then": "$$this",
                             "else": ["$$this"]
                        }}
                    ]
                }
            }
        }
    }},
    {"$project": {
        "coAuthors": {
            "$filter": {
                "input": "$coAuthors",
                "as": "co",
                "cond": {"$ne": ["$$co", "$_id"]}
            }
        },
        "affiliations": {
            "$filter": {
                "input": "$affiliations",
                "as": "aff",
                "cond": {"$gt": ["$$aff.affiliation", ""]}
            }
        },
        "keywords": {
            "en": "$keywords_en",
            "fr": "$keywords_fr"
        },
        "fundings": 1,
        "publications": 1,
        "thematics": 1
    }},
    {"$unwind": {"path": "$affiliations", "preserveNullAndEmptyArrays": True}},
    {
        "$group": {
            "_id": {"authors": "$_id", "aff": "$affiliations.affiliation"},
            "doc": {"$first":"$$ROOT"},
            "startDate": {"$min": "$affiliations.year"},
            "endDate": {"$max": "$affiliations.year"},
            "sources": {"$addToSet": "$affiliations.source"}
        }
    },
    {"$addFields": {
        "doc.affil": {
            "affiliation": "$_id.aff",
            "startDate": "$startDate",
            "endDate": "$endDate",
            "sources": "$sources",
        }
    }},
    {"$replaceRoot":{"newRoot":"$doc"}},
    {
        "$group": {
            "_id": "$_id",
            "doc": {"$first":"$$ROOT"},
            "affil": {
                "$addToSet": "$affil"
            }
        }
    },
    {"$addFields": {
        "doc.affiliations": "$affil"
    }},
    {"$replaceRoot":{"newRoot":"$doc"}},
    {"$project": {
        "coAuthors": 1,
        "affiliations": {
            "$filter": {
                "input": "$affiliations",
                "as": "aff",
                "cond": {"$gt": ["$$aff.affiliation", ""]}
            }
        },
        "keywords": 1,
        "fundings": 1,
        "publications": 1,
        "thematics": 1
    }},
    {"$out": "authors"}
]


publications_pipeline = [
    {"$match": {"is_french": True}},
    {"$addFields": {
        "language": {"$ifNull": ["$language", "default"]}
    }},
    {"$addFields": {
        "domains": {
            "$reduce": {
                "input": "$thematics",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{
                            "label": {
                                "en": "$$this.en_label",
                                "fr": "$$this.fr_label",
                                "default": {
                                    "$concat": [
                                        {"$ifNull": ["$$this.en_label", ""]},
                                        {
                                            "$cond": {
                                                "if": { "$gt": [ "$$this.en_label", "" ] },
                                                "then": " ",
                                                "else": ""
                                            }
                                        },
                                        {"$ifNull": ["$$this.fr_label", ""]}
                                    ]
                                }
                            },
                            "type": "$$this.reference",
                            "code": "$$this.code"
                        }]
                    ]
                }
            }
        },
        "certifications": {
            "$reduce": {
                "input": "$certifications",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{
                            "label": "$$this.certification_name",
                            "date": "$$this.certification_date"
                        }]
                    ]
                }
            }
        },
        "awards": {
            "$reduce": {
                "input": "$prizes",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{
                            "structure": "$$this.prize_institution",
                            "label": "$$this.prize_name",
                            "date": "$$this.prize_date",
                            "url": "$$this.prize_url",
                            "amount": "$$this.prize_amount",
                            "description": "$$this.prize_description"
                        }]
                    ]
                }
            }
        },
        "similarPublications": {
            "$reduce": {
                "input": "$similar_publications",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{
                            "target": "$$this.id_publication",
                            "score": "$$this.similarity_score"
                        }]
                    ]
                }

            }
        },
        "projects": {
            "$reduce": {
                "input": "$funding_info",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{"$toUpper": "$$this.funding_ref"}]
                    ]
                }
            }
        },
        "externalIds": {
            "$reduce": {
                "input": "$id_external",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{
                            "type": "$$this.id_type",
                            "id": "$$this.id_value"
                        }]
                    ]
                }
            }
        },
        "links": {
            "$reduce": {
                "input": "$links",
                "initialValue": [],
                "in": {
                    "$concatArrays": [
                        "$$value",
                        [{
                            "type": "$$this.link_type",
                            "url": "$$this.link_value"
                        }]
                    ]
                }
            }
        }
    }},
    {"$unwind": {"path": "$authors", "preserveNullAndEmptyArrays": True}},
    {"$addFields": {
        "authors.affiliations": "$authors.affiliations.id",
    }},
    {"$group": {
        "_id": "$_id",
        "doc": {"$first": "$$ROOT"},
        "authors": {
            "$addToSet": {
                "person": "$authors.id",
                "firstName": "$authors.first_name",
                "lastName": "$authors.last_name",
                "fullName": {
                    "$concat": [
                        "$authors.first_name",
                        " ",
                        "$authors.last_name"
                    ]
                },
                "role": "$authors.role",
                "affiliations": "$authors.affiliations"
            }
        }
    }},
    {"$addFields": {
        "doc.authors": "$authors"
    }},
    {"$replaceRoot": {"newRoot": "$doc"}},
    {"$addFields": {
         "affiliations": {
             "$reduce": {
                 "input": "$affiliations",
                 "initialValue": [],
                 "in": {
                     "$setUnion": [
                         "$$value",
                         ["$$this.id"]
                     ]
                 }
             }
         },
        "all_keywords": {
            "$setUnion": [{"$ifNull": ["$keywords_fr", []]}, {"$ifNull": ["$keywords_en", []]}]
        },
        "projects": {
            "$filter": {
               "input": "$projects",
               "as": "item",
               "cond": { "$ne": [ "$$item", "" ] }
            }
         }
    }},
    {"$project":
        {
            "authors": 1,
            "id": {"$let":{
                "vars":{"split": {"$split":["$id", "/"]}},
                "in": {
                    "$reduce":{
                        "input":{"$slice":["$$split", 1, {"$size":"$$split"}]},
                        "initialValue":{"$arrayElemAt":["$$split", 0]},
                        "in":{"$concat":["$$value", "%2f" ,"$$this"]}
                    }
                }
            }},
            "similarPublications": 1,
            "domains": 1,
            "affiliations": 1,
            "awards": 1,
            "certifications": 1,
            "projects": 1,
            "language": 1,
            "createdAt": "$created_at",
            "lastUpdated": "$modified_at",
            "citedBy": "$id_citations",
            "references": "$id_references",
            "focus": "$focus",
            "links": "$links",
            "externalIds": "$externalIds",
            "title": [{"k": "default", "v": {"$ifNull": ["$title", None]}}],
            "subtitle": [{"k": "default", "v": {"$ifNull": ["$subtitle", None]}}],
            "summary": [{"k": "default", "v": {"$ifNull": ["$summary", None]}}],
            "alternativeSummary": [{"k": "default", "v": {"$ifNull": ["$alternative_summary", None]}}],
            "productionType": {"$cond": [{"$eq": ["$genre", "these"]}, "thesis", "publication"]},
            "type": {"$ifNull": ["$genre", None]},
            "isOa": {"$ifNull": ["$is_oa", None]},
            "apc": {"$ifNull": ["$apc", None]},
            "isFrench": {"$ifNull": ["$is_french", None]},
            "publicationDate": {"$ifNull": ["$publication_date", {"$ifNull": ["$thesis_informations.defense_date", None]}]},
            "year": {"$year": {"$ifNull": ["$publication_date", {"$ifNull": ["$thesis_informations.defense_date", None]}]}},
            "submissionDate": {"$ifNull": ["$submission_date", None]},
            "doiUrl": {
                "$switch": {
                    "branches": [
                        {
                            "case": {"$eq": [{"$substr": ["$id", 0, 3]}, "doi"]},
                            "then": {"$concat": ["http://doi.org/", {"$substr": ["$id", 3, -1]}]}
                        },
                        {
                            "case": {"$eq": [{"$substr": ["$id", 0, 5]}, "these"]},
                            "then": {"$concat": ["http://www.theses.fr/", {"$substr": ["$id", 5, -1]}]}
                        },
                        {
                            "case": {"$eq": [{"$substr": ["$id", 0, 5]}, "sudoc"]},
                            "then": {"$concat": ["http://www.sudoc.fr/", {"$substr": ["$id", 5, -1]}]}
                        },
                   ],
                   "default": None
                }
            },
            "keywords": {
                "en": "$keywords_en",
                "fr": "$keywords_fr",
                "default": "$all_keywords"
            },
            "source": {
                "pagination": "$source.pagination",
                "issue": "$source.issue",
                "articleNumber": "$source.article_number",
                "title": "$source.source_title",
                "subtitle": "$source.source_sub_title",
                "isInDoaj": "$source.source_is_in_doaj",
                "isOa": "$source.source_is_oa",
                "type": "$source.source_genre",
                "publisher": "$source.publisher",
                "journalIssns": "$source.journal_issns"
            },
            "oaEvidence": {
                "hostType": "$oa_evidence.host_type",
                "version": "$oa_evidence.version",
                "updated": "$oa_evidence.updated",
                "url": "$oa_evidence.url",
                "pdfUrl": "$oa_evidence.url_for_pdf",
                "landingPageUrl": "$oa_evidence.url_for_landing_page",
                "license": "$oa_evidence.license"
            },
        }
    },
    {"$addFields": {
        "citedByCount": {
            "$cond": {
                "if": {"$isArray": "$citedBy"},
                "then": {"$size": "$citedBy"},
                "else": 0
            }
        },
        "referencesCount": {
            "$cond": {
                "if": {"$isArray": "$references"},
                "then": {"$size": "$references"},
                "else": 0
            }
        },
        "authorsCount": {
            "$cond": {
                "if": {"$isArray": "$authors"},
                "then": {"$size": "$authors"},
                "else": 0
            }
        },
        "title": {
            "$arrayToObject": "$title"
        },
        "subtitle": {
            "$arrayToObject": "$subtitle"
        },
        "summary": {
            "$arrayToObject": "$summary"
        },
        "alternativeSummary": {
            "$arrayToObject": "$alternativeSummary"
        },
    }},
    {"$out": "scanr"}
]
