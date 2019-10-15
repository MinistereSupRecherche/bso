"""Model for dataESR publications."""

dump_opencitations_schema = {
    "oci": {
        "type": "string"
    }
}

dump_openapc_schema = {
        "doi": {
            "type": "string"
        }
}

dump_unpaywall_schema = {
        "doi": {
            "type": "string"
        }
}

tasks_schema = {
        "id": {
            "type": "string"
        }
}

meta = {
    "description": "Meta data for database management",
    "type": "dict",
    "required": True,
    "default_setter": "meta",
    "coerce": "meta",
    "schema": {
        "id": {
            "description": "Unique identifier for the list item",
            "type": "string"
        },
        "created_at": {
            "description": "Start date of data validity",
            "type": "datetime",
            "example": "2018-01-01T00:00:00"
        },
        "modified_at": {
            "description": "Last modification date",
            "type": "datetime"
        },
        "created_by": {
            "description": "Initial data source",
            "type": "string"
        },
        "modified_by": {
            "description": "Last modification user",
            "type": "string"
        }
    }
}


oa_evidence = {
        "description": "",
        "type": "dict",
        "schema": {
            "host_type": {
                "description": "",
                "type": "string"
            },
            "is_oa": {
                "description": "",
                "type": "boolean"
            },
            "is_best": {
                "description": "",
                "type": "boolean"
            },
            "version": {
                "description": "",
                "type": "string"
            },
            "updated": {
                "description": "",
                "type": "datetime"
            },
            "url": {
                "description": "",
                "type": "string",
            },
            "url_for_pdf": {
                "description": "",
                "type": "string",
            },
            "url_for_landing_page": {
                "description": "",
                "type": "string",
            },
            "pmh_id": {
                "description": "",
                "type": "string",
            },
            "evidence": {
                "description": "",
                "type": "string",
            },
            "endpoint_id": {
                "description": "",
                "type": "string",
            },
            "repository_institution": {
                "description": "",
                "type": "string",
            },
            "license": {
                "description": "",
                "type": "string",
                "nullable": True
            }
        }
}

thematics = {
    "type": "dict",
    "schema": {
        "type": "dict",
        "schema": {
                "code": {
                        "description": "",
                        "type": "string"
                },
                "score": {
                        "description": "",
                        "type": "string"
                },
                "url": {
                        "description": "",
                        "type": "string"
                },
                "en_label": {
                        "description": "",
                        "type": "string"
                },
                "fr_label": {
                        "description": "",
                        "type": "string"
                },
                "reference": {
                        "description": "",
                        "type": "string"
                },
                "meta": meta
        }
    }
}

publications_schema = {
    "id": {
        "description": "",
        "type": "string",
        "required": True,
        "unique": True
    },
    "doi": {
        "description": "",
        "type": "string"
    },
    "id_hal": {
        "description": "",
        "type": "string"
    },
    "apc": {
        "description": "",
        "type": "float"
    },
    "doi_url": {
        "description": "",
        "type": "string",
    },
    "summary": {
        "description": "",
        "type": "string"
    },
    "fulltext": {
        "description": "",
        "type": "string"
    },
    "alternative_summary": {
        "description": "",
        "type": "string"
    },
    "title": {
        "description": "",
        "type": "string"
    },
    "sub_title": {
        "description": "",
        "type": "string"
    },
    "identified_authors": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "html_affiliations_info": {
        "description": "person identifier",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "institution_name": {
                    "description": "affiliation identifier",
                    "type": "string"
                },
                "structure_name": {
                    "description": "affiliation identifier",
                    "type": "string"
                },
                "start_date": {
                    "description": "A été affilié à partir de cette date",
                    "example": "2010-10-01T00:00:00",
                    "type": "datetime",
                },
                "address": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                },
                "country": {
                    "type": "string"
                },
                "meta": meta
            }
        }
    },
    "hal_authors_info": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "html_authors_info": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "last_name": {
                    "description": "last name of the person",
                    "type": "string"
                },
                "first_name": {
                    "description": "first name of the person",
                    "type": "string"
                },
                "full_name": {
                    "description": "full name of the person",
                    "type": "string"
                },
                "role": {
                    "type": "string"
                },
                "orcid": {
                    "description": "person identifier",
                    "type": "string"
                },
                "email": {
                    "description": "person identifier",
                    "type": "string"
                },
                "affiliations_info": {
                    "description": "person identifier",
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "institution_name": {
                                "description": "affiliation identifier",
                                "type": "string"
                            },
                            "structure_name": {
                                "description": "affiliation identifier",
                                "type": "string"
                            },
                            "address": {
                                "type": "string"
                            },
                            "city": {
                                "type": "string"
                            },
                            "country": {
                                "type": "string"
                            }
                        }
                    }
                },
                "meta": meta
            }
        }
    },
    "funding_info": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "funder": {
                    "type": "string"
                },
                "funding_ref": {
                    "type": "string"
                },
                "project_title": {
                    "type": "string"
                },
                "project_acronym": {
                    "type": "string"
                },
                "meta": meta
            }
        }
    },
    "affiliations": {
        "description": "affiliations ids",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {
                    "description": "affiliation identifier",
                    "type": "string"
                },
                "meta": meta
            }
        }
    },
    "projects": {
        "description": "projects ids",
        "type": "list",
        "schema": {
            "type": "string"
                }
    },
    "authors": {
        "description": "list of authors",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "last_name": {
                    "description": "last name of the person",
                    "type": "string"
                },
                "first_name": {
                    "description": "first name of the person",
                    "type": "string"
                },
                "full_name": {
                    "description": "full name of the person",
                    "type": "string"
                },
                "role": {
                    "description": "person identifier",
                    "type": "string"
                },
                "id": {
                    "description": "person identifier",
                    "type": "string"
                },
                "id_hal": {
                    "description": "person identifier",
                    "type": "string"
                },
                "docid_hal": {
                    "description": "person identifier",
                    "type": "string"
                },
                "orcid": {
                    "description": "person identifier",
                    "type": "string"
                },
                "email": {
                    "description": "person identifier",
                    "type": "string"
                },
                "affiliations_info": {
                    "description": "affiliations info",
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "institution_name": {
                                "description": "affiliation identifier",
                                "type": "string"
                            },
                            "structure_name": {
                                "description": "affiliation identifier",
                                "type": "string"
                            },
                            "address": {
                                "type": "string"
                            },
                            "city": {
                                "type": "string"
                            },
                            "country": {
                                "type": "string"
                            }
                        }
                    }
                },
                "affiliations": {
                    "description": "affiliations ids",
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "id": {
                                "description": "affiliation identifier",
                                "type": "string"
                            },
                            "meta": meta
                        }
                    }
                },
                "meta": meta
            }
        }
    },
    "thesis_informations": {
        "type": "dict",
        "schema": {
            "start_date": {
                "description": "",
                "type": "datetime"
            },
            "defense_date": {
                "type": "datetime"
            },
            "defense_place": {
                "type": "string"
            },
            "founder": {
                "type": "string"
            },
            "thesis_type": {
                "type": "string"
            }
        }
    },
    "updated": {
        "description": "",
        "type": "datetime"
    },
    "source": {
        "description": "",
        "type": "dict",
        "schema": {
            "pagination": {
                "description": "",
                "type": "string"
            },
            "issue": {
                "description": "",
                "type": "string"
            },
            "article_number": {
                "description": "",
                "type": "string"
            },
            "source_title": {
                "description": "",
                "type": "string"
            },
            "source_sub_title": {
                "description": "",
                "type": "string"
            },
            "source_is_in_doaj": {
                "description": "",
                "type": "boolean"
            },
            "source_is_oa": {
                "description": "",
                "type": "boolean"
            },
            "source_genre": {
                "description": "journal, book, theses ...",
                "type": "string"
            },
            "publisher": {
                "description": "",
                "type": "string"
            },
            "journal_issns": {
                "description": "",
                "type": "list",
                "schema": {
                    "type": "string",
                    "regex": "(....)-(....)"
                }
            }
        }
    },
    "oa_evidence": oa_evidence,
    "oa_locations": {
        "type": "list",
        "schema": oa_evidence
    },
    "oa_locations_history": {
        "type": "list",
        "schema": oa_evidence
    },
    "oa_host_type": {
                "description": "",
                "type": "string"
    },
    "genre": {
        "description": "Genre de la publication",
        "type": "string"
    },
    "language": {
        "description": "",
        "type": "string"
    },
    "data_sources": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "is_oa": {
        "description": "",
        "type": "boolean"
    },
    "first_time_seen_oa_date": {
        "description": "",
        "type": "datetime"
    },
    "is_french": {
        "description": "",
        "type": "boolean"
    },
    "persons_identified": {
        "description": "",
        "type": "boolean"
    },
    "structures_identified": {
        "description": "",
        "type": "boolean"
    },
    "id_external": {
        "description": "autres ids reperes pour la publication",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id_type": {
                    "description": "source de l'identifiant, p.ex HAL etc...",
                    "type": "string"
                },
                "id_value": {
                    "description": "",
                    "type": "string"
                },
                "meta": meta
            }
        }
    },
    "publication_date": {
        "description": "",
        "type": "datetime"
    },
    "keywords_en": {
        "description": "mot cles anglais",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "keywords_fr": {
        "description": "mot cles franais",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "id_citations": {
        "description": "id_publication des citations de la publication",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "id_references": {
        "description": "id_publication des references de la publication",
        "type": "list",
        "schema": {
            "type": "string"
        }
    },
    "thematics": {
        "description": "thematics",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "code": {
                    "description": "",
                    "type": "string"
                },
                "en_label": {
                    "description": "",
                    "type": "string"
                },
                "fr_label": {
                    "description": "",
                    "type": "string"
                },
                "reference": {
                    "description": "",
                    "type": "string"
                },
                "score": {
                    "description": "",
                    "type": "float"
                },
                "url": {
                    "description": "",
                    "type": "string"
                },
                "level": {
                    "description": "",
                    "type": "string"
                },
                "meta": meta
            }
        }
    },
    "links": {
        "description": "autresliens",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "link_type": {
                    "description": "",
                    "type": "string"
                },
                "link_value": {
                    "description": "",
                    "type": "string"
                },
                "meta": meta
            }
        }
    },
    "certifications": {
        "description": "certification",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "certification_name": {
                    "description": "",
                    "type": "string"
                },
                "certification_date": {
                    "description": "",
                    "type": "datetime"
                },
                "meta": meta
            }
        }
    },
    "prizes": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "meta": meta,
                "prize_name": {
                    "description": "",
                    "type": "string"
                },
                "prize_institution": {
                    "description": "",
                    "type": "string"
                },
                "prize_url": {
                    "description": "",
                    "type": "string"
                },
                "prize_description": {
                    "description": "",
                    "type": "string"
                },
                "prize_date": {
                    "description": "",
                    "type": "datetime",
                },
                "prize_amount": {
                    "description": "",
                    "type": "float"
                },
            }
        }
    },
    "similar_publications": {
        "description": "",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id_publication": {
                    "description": "",
                    "type": "string"
                },
                "similarity_score": {
                    "description": "",
                    "type": "number"
                },
                "meta": meta
            }
        }
    },
    "other_schema": {
        "description": "autresliens",
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "prop_type": {
                    "description": "",
                    "type": "string"
                },
                "prop_value": {
                    "description": "",
                    "type": "string"
                },
                "meta": meta
            }
        }
    }
}

notices_publications_schema = {
    "id": {
        "description": "Notice id",
        "type": "string",
        "required": True,
        "unique": True
    },
    "notice": {
        "description": "Notice",
        "type": "string",
        "required": True
    }
}
