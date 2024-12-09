class KindleClipping:
    def __init__(self, title, author, location, text):
        self.title = title
        self.author = author
        self.location = location
        self.text = text

def parse_clippings_file(file_path):
    """Parse the My Clippings.txt file and return a dictionary of books and their clippings."""
    clippings = {}
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read().split('==========')
        
    for entry in content:
        if not entry.strip():
            continue
            
        try:
            # Split into metadata and text
            parts = entry.strip().split('\n')
            if len(parts) < 4:
                continue
                
            # Parse title and author
            title_author = parts[0].strip()
            if '(' in title_author:
                title = title_author[:title_author.rfind('(')].strip()
                author = title_author[title_author.rfind('(')+1:title_author.rfind(')')].strip()
            else:
                title = title_author
                author = "Unknown"
                
            # Parse location
            metadata = parts[1].strip()
            location = metadata.split('|')[0].strip()
            
            # Get the highlight text
            text = parts[3].strip()
            
            # Create clipping object
            clipping = KindleClipping(title, author, location, text)
            
            # Add to dictionary
            if title not in clippings:
                clippings[title] = []
            clippings[title].append(clipping)
            
        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue
            
    return clippings

def get_book_clippings(file_path, book_title):
    """Get all clippings for a specific book."""
    all_clippings = parse_clippings_file(file_path)
    
    # Try to find exact match first
    if book_title in all_clippings:
        return all_clippings[book_title]
    
    # If no exact match, try case-insensitive partial match
    for title in all_clippings:
        if book_title.lower() in title.lower():
            return all_clippings[title]
    
    return []

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python clippings.py <path_to_clippings_file> <book_title>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    book_title = sys.argv[2]
    
    clippings = get_book_clippings(file_path, book_title)
    
    if not clippings:
        print(f"No clippings found for book: {book_title}")
    else:
        for clip in clippings:
            print(clip.text)
