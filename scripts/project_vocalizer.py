#!/usr/bin/env python3
"""
Project Vocalizer v1.0
Fokus: Transformering af aktive projekter til mundret tekst til voice-interfacet.
Del af V7.1 Real-world API Integration.
"""
import json
import os
import notion_read_projects

def get_projects_vocalized():
    projects = notion_read_projects.get_active_projects()
    
    if not projects:
        return "Jeg kunne ikke finde nogle aktive projekter i din Notion. "
    
    # Fokusér på top prioriteter
    p0_projects = [p for p in projects if p['priority'] == 'P0']
    
    if p0_projects:
        intro = f"I din Notion er det vigtigste projekt lige nu {p0_projects[0]['name']}. "
    else:
        intro = "Du har et par aktive projekter i din Notion. "
        
    return intro

if __name__ == "__main__":
    print(get_projects_vocalized())
