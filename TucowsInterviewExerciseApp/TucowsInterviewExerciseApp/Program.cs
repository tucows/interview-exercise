using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Net;
using System.Text;
using System.IO;

namespace TucowsInterviewExerciseApp
{
    class Program
    {
        // Apis base urls
        private const string QUOTES_API_URL = "http://api.forismatic.com/api/1.0/";
        private const string IMAGES_API_BASIC_URL = "https://picsum.photos";

        static void Main(string[] args)
        {
            string userInput = "";

            QuoteAPI();
            ImageAPI();

            do
            {
                Menu();
                userInput = Console.ReadLine();

                switch (userInput)
                {
                    case "1": // Random quote and image
                        QuoteAPI();
                        ImageAPI();
                        break;
                    case "2": // Random quote with grayscale image
                        QuoteAPI();
                        ImageAPI(true);
                        break;
                    case "3": // Random image with a specified quote key
                        Console.WriteLine("Please enter a key (maximum 6 digits)\n");
                        string key = Console.ReadLine();
                        try
                        {
                            if (int.Parse(key) > 0 && int.Parse(key) <= 999999) QuoteAPI(key);
                            else throw new Exception();

                        }
                        catch
                        {
                            Console.WriteLine("something wrong with the key, calling random qoute..");
                            QuoteAPI();
                        }
                        ImageAPI();
                        break;
                    case "4":
                        Console.WriteLine("Thank you for using this app.");
                        break;
                    default: // any other choice is not accepted
                        Console.WriteLine("Undefined chioce, please try again..");
                        break;

                }
            } while (userInput != "4");

        }

        static void Menu()
        {
            Console.Write("\n\n");
            Console.Write("Random image and quote display\n\n" +
                "1. Random quote and image.\n" +
                "2. Random quote with grayscale image. (Optional)\n" +
                "3. Random image with a specified quote key. (Optional)\n" +
                "4. Exit\n\n" +
                "Please Enter your choice...\n");
        }

        static void ImageAPI(bool grayscale = false)
        {
            HttpClient client = new HttpClient();
            //  string id = null;
            string imageApiURL = IMAGES_API_BASIC_URL + "/200/150";


            client.BaseAddress = new Uri(imageApiURL);

            // adding headers so the website allow the http client to retrieve images 
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept", "text/html,application/xhtml+xml,application/xml");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept-Encoding", "gzip, deflate");
            client.DefaultRequestHeaders.TryAddWithoutValidation("User-Agent", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept-Charset", "ISO-8859-1");

            // Console.WriteLine(imageApiURL);

            // preparing parameters
            string requestParams = grayscale ? "?grayscale" : "";


            HttpResponseMessage response = client.GetAsync(requestParams).Result;
            if (response.IsSuccessStatusCode)
            {
                // save the image in temp file in the project directory, then display it
                var fileName = ".\\tempImg.jpg";
                var responseContent = response.Content.ReadAsByteArrayAsync().Result;
                File.WriteAllBytes(fileName, responseContent);
                string argument = "/open, \"" + fileName + "\"";
                System.Diagnostics.Process.Start("explorer.exe", argument);

                //Console.WriteLine(responseContent);
            }
            else
            {
                Console.WriteLine("Error: " + response.StatusCode);
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

        }

        static void QuoteAPI(string key = "")
        {
            // preparing params
            string requestParams = $"?method=getQuote&format=json&key={key}&lang=en";

            HttpClient client = new HttpClient();
            client.BaseAddress = new Uri(QUOTES_API_URL);

            client.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));

            //get the response
            HttpResponseMessage response = client.GetAsync(requestParams).Result;

            if (response.IsSuccessStatusCode)
            {
                var responseContent = response.Content.ReadAsStringAsync().Result;
                //   Console.WriteLine(responseContent);

                try
                {
                    var responseObj = JsonSerializer.Deserialize<ResponseObject>(responseContent);

                    Console.WriteLine();
                    Console.WriteLine();
                    Console.WriteLine("Quote: " + responseObj.quoteText);
                    Console.WriteLine("Quote Author: " + responseObj.quoteAuthor);
                    Console.WriteLine("Sender: " + responseObj.senderName);
                    Console.WriteLine("Sender Link: " + responseObj.senderLink);
                    Console.WriteLine("Quote Link: " + responseObj.quoteLink);
                }
                catch (Exception e)
                {
                    Console.WriteLine("Something went wrong with the quote service, please try again..\n");
                }

            }
            else
            {
                Console.WriteLine("Error: " + response.StatusCode);
            }

        }
    }


    // Quote Model
    public class ResponseObject
    {

        public string quoteText { get; set; }
        public string quoteAuthor { get; set; }
        public string senderName { get; set; }
        public string senderLink { get; set; }
        public string quoteLink { get; set; }
    }
}
