import axios from 'axios';
import * as xml2js from 'xml2js';
import * as fs from 'fs';

interface Book {
  title: string;
  author: string;
  link: string;
  pubDate: string;
  isbn?: string;
  goodreadsId?: string;
  pages?: number;
  rating?: number;
  userRating?: number;
  readStatus?: string;
  publicationYear?: number;
  description?: string;
  openLibraryId?: string;
}

/**
 * Fetches a Goodreads RSS feed from the provided URL
 * @param url The URL of the Goodreads RSS feed
 * @returns The raw XML content of the feed
 */
async function fetchGoodreadsRSS(url: string): Promise<string> {
  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching Goodreads RSS feed:', error);
    throw error;
  }
}

/**
 * Parses the XML content of a Goodreads RSS feed
 * @param xmlContent The XML content to parse
 * @returns Parsed JavaScript object
 */
async function parseXML(xmlContent: string): Promise<any> {
  const parser = new xml2js.Parser({ 
    explicitArray: false,
    // Preserve all namespaces for proper parsing
    xmlns: true
  });
  return new Promise((resolve, reject) => {
    parser.parseString(xmlContent, (err, result) => {
      if (err) {
        reject(err);
      } else {
        resolve(result);
      }
    });
  });
}

/**
 * Extracts book information from the parsed RSS feed
 * @param parsedData The parsed RSS feed data
 * @returns Array of Book objects
 */
function extractBooks(parsedData: any): Book[] {
  if (!parsedData.rss || !parsedData.rss.channel || !parsedData.rss.channel.item) {
    console.error('Invalid RSS feed format');
    return [];
  }

  const items = Array.isArray(parsedData.rss.channel.item) 
    ? parsedData.rss.channel.item 
    : [parsedData.rss.channel.item];

  return items.map((item: any) => {
    // Parse fields that may come as objects with a _ property
    const title = typeof item.title === 'object' && item.title._ 
      ? item.title._ 
      : item.title || 'Untitled';

    const link = typeof item.link === 'object' && item.link._ 
      ? item.link._ 
      : item.link || '';

    const pubDate = typeof item.pubDate === 'object' && item.pubDate._ 
      ? item.pubDate._ 
      : item.pubDate || '';

    // Parse the description to extract metadata
    const descriptionText = typeof item.description === 'object' && item.description._ 
      ? item.description._ 
      : item.description || '';
    
    // Extract ISBN
    const isbnMatch = descriptionText.match(/(\d{10}|\d{13})/);
    const isbn = isbnMatch ? isbnMatch[1] : undefined;
    
    // Extract pages
    const pagesMatch = descriptionText.match(/(\d+) pages/i) || descriptionText.match(/^(\d+)$/m);
    const pages = pagesMatch ? parseInt(pagesMatch[1], 10) : undefined;
    
    // Extract author - from the description or from dc:creator
    let author = item['dc:creator'] || '';
    if (!author && descriptionText) {
      const authorMatch = descriptionText.match(/author:\s*([^<]+)/i);
      if (authorMatch) {
        author = authorMatch[1].trim();
      }
    }
    
    // Extract user rating
    const userRatingMatch = descriptionText.match(/rating:\s*(\d+)/i);
    const userRating = userRatingMatch ? parseInt(userRatingMatch[1], 10) : undefined;
    
    // Extract average rating
    const avgRatingMatch = descriptionText.match(/average rating:\s*(\d+\.\d+)/i);
    const rating = avgRatingMatch ? parseFloat(avgRatingMatch[1]) : undefined;
    
    // Extract read status
    const statusMatch = descriptionText.match(/shelves:\s*([^<]+)/i);
    const readStatus = statusMatch ? statusMatch[1].toLowerCase().trim() : undefined;
    
    // Extract publication year
    const yearMatch = descriptionText.match(/book published:\s*(\d{4})/i);
    const publicationYear = yearMatch ? parseInt(yearMatch[1], 10) : undefined;

    return {
      title,
      author: author || 'Unknown Author',
      link,
      pubDate,
      isbn,
      pages,
      rating,
      userRating,
      readStatus,
      publicationYear,
      description: descriptionText.trim() || undefined
    };
  });
}

/**
 * Saves the extracted book data to a JSON file
 * @param books Array of Book objects
 * @param outputPath Path to save the JSON file
 */
function saveToJSON(books: Book[], outputPath: string): void {
  fs.writeFileSync(outputPath, JSON.stringify(books, null, 2));
  console.log(`Saved ${books.length} books to ${outputPath}`);
}

/**
 * Logs a sample of the extracted books for debugging
 * @param books Array of Book objects
 */
function logSampleBooks(books: Book[]): void {
  if (books.length === 0) {
    console.log('No books found');
    return;
  }

  console.log('\nSample of extracted books:');
  const sampleSize = Math.min(3, books.length);
  for (let i = 0; i < sampleSize; i++) {
    const book = books[i];
    console.log(`\n[Book ${i + 1}]`);
    console.log(`Title: ${book.title}`);
    console.log(`Author: ${book.author}`);
    console.log(`ISBN: ${book.isbn || 'N/A'}`);
    console.log(`OpenLibrary ID: ${book.openLibraryId || 'N/A'}`);
    console.log(`Status: ${book.readStatus || 'N/A'}`);
    console.log(`Rating: ${book.rating || 'N/A'}`);
    console.log(`User Rating: ${book.userRating || 'N/A'}`);
    console.log(`Publication Year: ${book.publicationYear || 'N/A'}`);
    console.log(`Pages: ${book.pages || 'N/A'}`);
  }
  console.log('');
}

/**
 * Fetches all books from a Goodreads RSS feed by paginating through all available pages
 * @param baseUrl The base URL of the Goodreads RSS feed
 * @param limit Maximum number of books to fetch (optional)
 * @returns Array of all books from all pages
 */
async function fetchAllBooks(baseUrl: string, limit?: number): Promise<Book[]> {
  let page = 1;
  let allBooks: Book[] = [];
  let hasMoreBooks = true;

  console.log('Starting to fetch all pages...');
  if (limit) {
    console.log(`Will fetch up to ${limit} books`);
  }

  while (hasMoreBooks) {
    // If we have a limit and we've reached it, stop fetching
    if (limit && allBooks.length >= limit) {
      console.log(`Reached limit of ${limit} books, stopping pagination`);
      break;
    }

    const pageUrl = `${baseUrl}${baseUrl.includes('?') ? '&' : '?'}page=${page}`;
    console.log(`Fetching page ${page}...`);

    try {
      const xmlContent = await fetchGoodreadsRSS(pageUrl);
      const parsedData = await parseXML(xmlContent);
      const books = extractBooks(parsedData);

      if (books.length === 0) {
        hasMoreBooks = false;
      } else {
        // If we have a limit, only take what we need
        if (limit) {
          const remaining = limit - allBooks.length;
          allBooks = allBooks.concat(books.slice(0, remaining));
          console.log(`Added ${Math.min(books.length, remaining)} books from page ${page}`);
        } else {
          allBooks = allBooks.concat(books);
          console.log(`Added ${books.length} books from page ${page}`);
        }
        
        page++;

        // Add a small delay to avoid hitting rate limits
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    } catch (error) {
      console.error(`Error fetching page ${page}:`, error);
      hasMoreBooks = false;
    }
  }

  console.log(`Finished fetching pages. Total books found: ${allBooks.length}`);
  return allBooks;
}

/**
 * Extracts the Goodreads book ID from a book URL
 * @param url The Goodreads book URL
 * @returns The book ID or undefined if not found
 */
function extractGoodreadsId(url: string): string | undefined {
  const match = url.match(/\/show\/(\d+)/);
  return match ? match[1] : undefined;
}

/**
 * Rate-limited function to fetch OpenLibrary ID for a given book
 * @param book The book object containing title, author, and other metadata
 * @param delayMs Delay between API calls in milliseconds
 * @returns Promise with the OpenLibrary ID or undefined if not found
 */
async function fetchOpenLibraryId(book: Book, delayMs: number = 1000): Promise<string | undefined> {
  try {
    // Try searching by title and author first
    const query = `${book.title} ${book.author}`.replace(/[^\w\s]/g, ' ');
    const searchResponse = await axios.get(`https://openlibrary.org/search.json?q=${encodeURIComponent(query)}`);
    const searchData = searchResponse.data;
    
    if (searchData.docs && searchData.docs.length > 0) {
      // Try to find an exact match by title and author
      const exactMatch = searchData.docs.find((doc: any) => {
        const titleMatch = doc.title && doc.title.toLowerCase() === book.title.toLowerCase();
        const authorMatch = doc.author_name && doc.author_name.some((name: string) => 
          name.toLowerCase() === book.author.toLowerCase()
        );
        return titleMatch && authorMatch;
      });
      
      if (exactMatch) {
        // Try to get the work ID first
        if (exactMatch.key && exactMatch.key.startsWith('/works/')) {
          const workId = exactMatch.key.replace('/works/', '');
          console.log(`Found OpenLibrary work ID for "${book.title}": ${workId}`);
          return workId;
        }
        
        // If no work ID, try edition ID
        if (exactMatch.edition_key && exactMatch.edition_key.length > 0) {
          const editionId = exactMatch.edition_key[0];
          console.log(`Found OpenLibrary edition ID for "${book.title}": ${editionId}`);
          return editionId;
        }
      }
      
      // If no exact match, try the first result
      const firstResult = searchData.docs[0];
      if (firstResult.key && firstResult.key.startsWith('/works/')) {
        const workId = firstResult.key.replace('/works/', '');
        console.log(`Found OpenLibrary work ID for "${book.title}" (best match): ${workId}`);
        return workId;
      }
      
      if (firstResult.edition_key && firstResult.edition_key.length > 0) {
        const editionId = firstResult.edition_key[0];
        console.log(`Found OpenLibrary edition ID for "${book.title}" (best match): ${editionId}`);
        return editionId;
      }
    }
    
    console.log(`No OpenLibrary ID found for "${book.title}"`);
    return undefined;
  } catch (error) {
    console.error(`Error fetching OpenLibrary data for "${book.title}":`, error);
    return undefined;
  } finally {
    // Wait for the specified delay before the next call
    await new Promise(resolve => setTimeout(resolve, delayMs));
  }
}

/**
 * Adds OpenLibrary IDs to books
 * @param books Array of Book objects
 * @param delayMs Delay between API calls in milliseconds
 * @returns Promise with updated books array
 */
async function addOpenLibraryIds(books: Book[], delayMs: number = 1000): Promise<Book[]> {
  console.log(`Starting to fetch OpenLibrary IDs for ${books.length} books...`);
  console.log(`Rate limiting: ${delayMs}ms between API calls`);
  
  const updatedBooks: Book[] = [];
  let processedCount = 0;
  let foundCount = 0;
  
  for (const book of books) {
    // Extract Goodreads ID from the book URL
    const goodreadsId = extractGoodreadsId(book.link);
    if (goodreadsId) {
      book.goodreadsId = goodreadsId;
    }
    
    const openLibraryId = await fetchOpenLibraryId(book, delayMs);
    if (openLibraryId) {
      foundCount++;
    }
    updatedBooks.push({
      ...book,
      openLibraryId
    });
    
    processedCount++;
    if (processedCount % 10 === 0) {
      console.log(`Processed ${processedCount}/${books.length} books (found ${foundCount} OpenLibrary IDs)`);
    }
  }
  
  console.log(`Finished fetching OpenLibrary IDs. Found ${foundCount} IDs out of ${processedCount} books`);
  return updatedBooks;
}

/**
 * Main function to process a Goodreads RSS feed
 * @param feedUrl URL of the Goodreads RSS feed
 * @param outputPath Path to save the output JSON file
 * @param debug Whether to log debug information
 * @param openLibraryDelayMs Delay between OpenLibrary API calls in milliseconds
 * @param limit Maximum number of books to process (optional)
 */
async function processGoodreadsRSS(
  feedUrl: string, 
  outputPath: string, 
  debug: boolean = false,
  openLibraryDelayMs: number = 1000,
  limit?: number
): Promise<void> {
  try {
    console.log(`Fetching Goodreads RSS feed from: ${feedUrl}`);
    
    // Fetch books from all pages, respecting the limit if set
    const books = await fetchAllBooks(feedUrl, limit);
    
    console.log(`Found ${books.length} books in total`);
    
    // Add OpenLibrary IDs
    const booksWithOpenLibraryIds = await addOpenLibraryIds(books, openLibraryDelayMs);
    
    // Log a sample of the extracted books
    if (debug || books.length > 0) {
      logSampleBooks(booksWithOpenLibraryIds);
    }
    
    saveToJSON(booksWithOpenLibraryIds, outputPath);
  } catch (error) {
    console.error('Error processing Goodreads RSS feed:', error);
  }
}

// Example usage and argument parsing
const args = process.argv.slice(2);
let feedUrl = 'https://www.goodreads.com/review/list_rss/YOUR_USER_ID?shelf=read';
let outputPath = 'goodreads-books.json';
let debug = false;
let openLibraryDelayMs = 1000;
let limit: number | undefined;

// Parse command line arguments
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  
  if (arg === '--debug') {
    debug = true;
  } else if (arg === '--openlibrary-delay' && i + 1 < args.length) {
    const value = parseInt(args[++i], 10);
    if (!isNaN(value)) {
      openLibraryDelayMs = value;
    }
  } else if (arg === '--limit' && i + 1 < args.length) {
    const value = parseInt(args[++i], 10);
    if (!isNaN(value)) {
      limit = value;
    }
  } else if (!arg.startsWith('--')) {
    // Positional arguments
    if (feedUrl === 'https://www.goodreads.com/review/list_rss/YOUR_USER_ID?shelf=read') {
      feedUrl = arg;
    } else if (outputPath === 'goodreads-books.json') {
      outputPath = arg;
    }
  }
}

if (process.argv.includes('--help') || process.argv.includes('-h')) {
  console.log(`
Usage: ts-node index.ts [feedUrl] [outputPath] [--debug] [--openlibrary-delay <ms>] [--limit <n>]

  feedUrl              URL of the Goodreads RSS feed (default: ${feedUrl})
  outputPath           Path to save the output JSON file (default: ${outputPath})
  --debug              Enable debug logging
  --openlibrary-delay  Delay between OpenLibrary API calls in milliseconds (default: 1000)
  --limit              Maximum number of books to process

Example:
  ts-node index.ts https://www.goodreads.com/review/list_rss/123456?shelf=read my-books.json --openlibrary-delay 2000 --limit 10
  `);
} else {
  processGoodreadsRSS(feedUrl, outputPath, debug, openLibraryDelayMs, limit)
    .then(() => console.log('Done!'))
    .catch(err => console.error('Failed to process feed:', err));
}

