<?php

/**
 * Displays site name.
 */
function site_name()
{
    echo config('name');
}

/**
 * Displays site url provided in config.
 */
function site_url()
{
    echo config('site_url');
}

/**
 * Displays site version.
 */
function site_version()
{
    echo config('version');
}

/**
 * Website navigation.
 */
function nav_menu()
{
    $nav_menu = '';
    $nav_items = config('nav_menu');
    
    foreach ($nav_items as $uri => $name) {
        $uri = $uri . ".html";
        $query_string = str_replace('page=', '', $_SERVER['QUERY_STRING'] ?? '');
        $class = $query_string == $uri ? ' active' : '';
        $url = config('site_url') . '/' . '?page=' . $uri;
        
        // Add nav item to list. See the dot in front of equal sign (.=)
        $nav_menu .= '<li class="nav-item"><a href="' . $url . '" title="' . $name . '" class="nav-link ' . $class . '">' . $name . '</a></li>';
    }

    echo $nav_menu;
}

/**
 * Displays page title. It takes the data from
 * URL, it replaces the hyphens with spaces and
 * it capitalizes the words.
 */
function page_title()
{
    $page = isset($_GET['page']) ? htmlspecialchars($_GET['page']) : 'Home';

    echo ucwords(str_replace(array('-', '.html'), ' ', $page));
}

/**
 * Displays page content. It takes the data from
 * the static pages inside the pages/ directory.
 * When not found, display the 404 error page.
 */
function page_content()
{
    $page = isset($_GET['page']) ? $_GET['page'] : 'home.html';
    $page = htmlspecialchars($page, ENT_QUOTES, 'UTF-8');
    $path = getcwd() . '/' . config('content_path') . '/' . $page;
    //print($path);

    if (!file_exists($path) || !is_file($path)) {
        $path = getcwd() . '/' . config('content_path') . '/404.html';
        echo file_get_contents($path);
    } elseif (!in_array($page, pages_list())) {
        $content = '<section class="notfound-section text-center" id="notfound"><div class="container px-4 px-lg-5"><div class="row gx-4 gx-lg-5 justify-content-center"><div class="col-lg-8"><h2 class="text-white mb-4">' . $page . '</h2><p class="text-white-50 mt-5 mb-5">' . file_get_contents($path) . '</p></div></div></div></section>';
        echo $content;
    } else {
        echo file_get_contents($path);
    }

}

/**
 * Starts everything and displays the template.
 */
function init()
{
    require config('template_path') . '/template.php';
}

function pages_list()
{
    $names = array_keys(config('nav_menu'));
    $files = array_map(function($val) { return $val . '.html'; }, $names);

    return $files;
}